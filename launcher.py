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

def is_port_open(port=PORT):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            return s.connect_ex(('127.0.0.1', port)) == 0
    except Exception:
        return False

def start_django_server():
    if is_port_open(PORT):
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
    httpd = make_server('127.0.0.1', PORT, application, handler_class=QuietHandler)
    httpd.serve_forever()

def launch_app_window():
    if not is_port_open(PORT):
        server_thread = threading.Thread(target=start_django_server, daemon=True)
        server_thread.start()

        for _ in range(20):
            time.sleep(0.5)
            if is_port_open(PORT):
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
        subprocess.Popen([browser_binary, f'--app={APP_URL}', '--window-size=1280,800'])
    else:
        webbrowser.open(APP_URL)

if __name__ == '__main__':
    launch_app_window()
