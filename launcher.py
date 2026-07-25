"""
launcher.py — EduManage অফলাইন লঞ্চার
=======================================
১. লোকাল Django সার্ভার চালু করে (127.0.0.1:8000)
২. ব্যাকগ্রাউন্ডে সিঙ্ক ম্যানেজার শুরু করে
৩. ব্রাউজারে অ্যাপ খোলে (app mode)
"""
import os
import sys
import threading
import time
import socket
import webbrowser
import subprocess

# Handle base directory for both regular Python and PyInstaller frozen .exe
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, BASE_DIR)
os.chdir(BASE_DIR)

PORT = 8000
APP_URL = f"http://127.0.0.1:{PORT}/"

# ──────────────────────────────────────────────
#  পোর্ট চেক
# ──────────────────────────────────────────────
def is_port_open(port=PORT):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            return s.connect_ex(('127.0.0.1', port)) == 0
    except Exception:
        return False


def find_free_port(start=8000, end=8020):
    """ব্যবহারযোগ্য পোর্ট খোঁজে।"""
    for p in range(start, end):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', p)) != 0:
                return p
    return start


# ──────────────────────────────────────────────
#  Django সার্ভার
# ──────────────────────────────────────────────
def start_django_server(port=PORT):
    if is_port_open(port):
        return
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_management.settings')
    import django
    django.setup()

    from django.core.wsgi import get_wsgi_application
    from django.contrib.staticfiles.handlers import StaticFilesHandler
    from wsgiref.simple_server import make_server, WSGIRequestHandler

    class QuietHandler(WSGIRequestHandler):
        def log_message(self, format, *args):
            pass

    application = StaticFilesHandler(get_wsgi_application())
    httpd = make_server('127.0.0.1', port, application, handler_class=QuietHandler)
    print(f"[EduManage] ✅ সার্ভার চলছে → http://127.0.0.1:{port}/")
    httpd.serve_forever()


# ──────────────────────────────────────────────
#  ব্যাকগ্রাউন্ড সিঙ্ক ম্যানেজার
# ──────────────────────────────────────────────
def start_sync_manager():
    """ব্যাকগ্রাউন্ডে সিঙ্ক ম্যানেজার শুরু করে।"""
    try:
        from sync_manager import SyncManager
        manager = SyncManager()
        manager.start()
        print("[EduManage] 🔄 সিঙ্ক ম্যানেজার চালু হয়েছে।")
        return manager
    except Exception as e:
        print(f"[EduManage] ⚠️ সিঙ্ক ম্যানেজার শুরু করা যায়নি: {e}")
        return None


# ──────────────────────────────────────────────
#  ব্রাউজার লঞ্চ
# ──────────────────────────────────────────────
def launch_app_window(port=PORT):
    app_url = f"http://127.0.0.1:{port}/"

    if not is_port_open(port):
        server_thread = threading.Thread(target=start_django_server, args=(port,), daemon=True)
        server_thread.start()

        print("[EduManage] সার্ভার চালু হচ্ছে...")
        for _ in range(40):
            time.sleep(0.5)
            if is_port_open(port):
                break

    # Look for Microsoft Edge, Google Chrome, or Brave standalone app mode
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        os.path.expanduser(r"~\AppData\Local\Microsoft\Edge\Application\msedge.exe")
    ]
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
    ]
    brave_paths = [
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
        os.path.expanduser(r"~\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe")
    ]

    browser_binary = None
    for path in edge_paths + chrome_paths + brave_paths:
        if os.path.exists(path):
            browser_binary = path
            break

    if browser_binary:
        subprocess.Popen([browser_binary, f'--app={app_url}', '--window-size=1280,800'])
    else:
        webbrowser.open(app_url)

    print(f"[EduManage] 🌐 ব্রাউজার খোলা হয়েছে → {app_url}")


# ──────────────────────────────────────────────
#  মেইন এন্ট্রিপয়েন্ট
# ──────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 50)
    print("   EduManage — অফলাইন স্কুল ম্যানেজমেন্ট সিস্টেম")
    print("=" * 50)

    # ১. পোর্ট চেক করা
    if is_port_open(PORT):
        print(f"[EduManage] পোর্ট {PORT} ইতিমধ্যে ব্যবহার হচ্ছে।")
    else:
        # Django সার্ভার থ্রেডে চালু
        server_thread = threading.Thread(target=start_django_server, args=(PORT,), daemon=True)
        server_thread.start()

        # সার্ভার রেডি হওয়ার অপেক্ষা
        for _ in range(40):
            time.sleep(0.5)
            if is_port_open(PORT):
                break

    # ২. সিঙ্ক ম্যানেজার শুরু (ব্যাকগ্রাউন্ডে)
    sync_mgr = start_sync_manager()

    # ৩. ব্রাউজার খোলা
    launch_app_window(PORT)

    # ৪. প্রধান থ্রেড জীবিত রাখা (daemon threads চালু রাখতে)
    print("[EduManage] চলছে... (এই উইন্ডো বন্ধ করবেন না)")
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n[EduManage] বন্ধ হচ্ছে...")
        if sync_mgr:
            sync_mgr.stop()
