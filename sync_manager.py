"""
sync_manager.py
===============
ব্যাকগ্রাউন্ড সিঙ্ক ম্যানেজার।
লোকাল সার্ভার চললে এটি ব্যাকগ্রাউন্ডে চলে এবং
নির্দিষ্ট বিরতিতে অনলাইন সার্ভারে ডেটা পাঠায়।

ব্যবহার:
    from sync_manager import SyncManager
    manager = SyncManager()
    manager.start()
"""
import os
import sys
import json
import time
import socket
import logging
import threading
import datetime
import urllib.request
import urllib.error

# ──────────────────────────────────────────────
#  কনফিগারেশন (settings.py থেকেও ওভাররাইড করা যাবে)
# ──────────────────────────────────────────────
ONLINE_SERVER_URL = os.environ.get('ONLINE_SERVER_URL', 'https://m-100184.onrender.com')
SYNC_API_KEY = os.environ.get('SYNC_API_KEY', 'offline-sync-secret-key-change-me')
SYNC_INTERVAL_SECONDS = int(os.environ.get('SYNC_INTERVAL_SECONDS', 900))  # ১৫ মিনিট
SYNC_TIMEOUT_SECONDS = 30
CONNECTIVITY_CHECK_HOST = 'google.com'
CONNECTIVITY_CHECK_PORT = 80

logging.basicConfig(
    level=logging.INFO,
    format='[SyncManager] %(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('sync_manager')


# ──────────────────────────────────────────────
#  ইন্টারনেট সংযোগ চেক
# ──────────────────────────────────────────────
def has_internet(host=CONNECTIVITY_CHECK_HOST, port=CONNECTIVITY_CHECK_PORT, timeout=3):
    """ইন্টারনেট আছে কিনা দ্রুত চেক করে।"""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except (socket.error, OSError):
        return False


# ──────────────────────────────────────────────
#  Django সেটআপ (যদি standalone চলে)
# ──────────────────────────────────────────────
def _setup_django():
    if not os.environ.get('DJANGO_SETTINGS_MODULE'):
        base = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, base)
        os.environ['DJANGO_SETTINGS_MODULE'] = 'school_management.settings'
    try:
        import django
        if not django.apps.registry.apps.ready:
            django.setup()
    except Exception:
        pass


# ──────────────────────────────────────────────
#  মডেল ডেটা সংগ্রহ
# ──────────────────────────────────────────────
def _collect_local_data():
    """লোকাল DB থেকে সিঙ্কযোগ্য ডেটা সংগ্রহ করে।"""
    from django.core import serializers

    payload = {'models': {}}
    total = 0

    try:
        try:
            from apps.users.models import StudentAdmission as StudentModel
        except ImportError:
            from apps.users.models import Student as StudentModel
        students = StudentModel.objects.all()
        payload['models']['students'] = json.loads(serializers.serialize('json', students))
        total += len(payload['models']['students'])
    except Exception as e:
        logger.warning(f"Student collect error: {e}")

    try:
        try:
            from apps.academics.models import ClassRoom as ClassModel
        except ImportError:
            from apps.academics.models import Class as ClassModel
        classes = ClassModel.objects.all()
        payload['models']['classes'] = json.loads(serializers.serialize('json', classes))
        total += len(payload['models']['classes'])

        try:
            from apps.academics.models import Subject
            subjects = Subject.objects.all()
            payload['models']['subjects'] = json.loads(serializers.serialize('json', subjects))
            total += len(payload['models']['subjects'])
        except Exception:
            pass
    except Exception as e:
        logger.warning(f"Academics collect error: {e}")

    payload['synced_at'] = datetime.datetime.utcnow().isoformat() + 'Z'
    payload['total_records'] = total
    return payload, total


# ──────────────────────────────────────────────
#  সিঙ্ক পাঠানো
# ──────────────────────────────────────────────
def run_sync_now():
    """
    এখনই একবার সিঙ্ক চালায়।
    Returns: dict with status and details
    """
    _setup_django()

    if not has_internet():
        logger.info("কোনো ইন্টারনেট নেই — সিঙ্ক এড়িয়ে গেল।")
        return {'status': 'skipped', 'reason': 'no_internet'}

    start_time = time.time()
    try:
        payload, total = _collect_local_data()

        if total == 0:
            logger.info("সিঙ্কের জন্য কোনো রেকর্ড নেই।")
            return {'status': 'skipped', 'reason': 'no_records'}

        data = json.dumps(payload, ensure_ascii=False, default=str).encode('utf-8')
        url = f"{ONLINE_SERVER_URL.rstrip('/')}/api/sync/push/"

        req = urllib.request.Request(
            url,
            data=data,
            headers={
                'Content-Type': 'application/json',
                'X-Sync-API-Key': SYNC_API_KEY,
                'User-Agent': 'EduManage-OfflineSync/1.0',
            },
            method='POST'
        )

        with urllib.request.urlopen(req, timeout=SYNC_TIMEOUT_SECONDS) as resp:
            response_data = json.loads(resp.read().decode('utf-8'))

        duration = round(time.time() - start_time, 2)
        logger.info(f"✅ সিঙ্ক সফল! {total} রেকর্ড → {duration}s")

        # DB তে লগ করা
        try:
            from apps.sync.models import SyncLog, SyncConfig
            SyncLog.objects.create(
                status='success',
                direction='push',
                records_synced=total,
                duration_seconds=duration,
            )
            cfg = SyncConfig.get_config()
            from django.utils import timezone
            cfg.last_successful_sync = timezone.now()
            cfg.save(update_fields=['last_successful_sync'])
        except Exception as log_err:
            logger.warning(f"Log save error: {log_err}")

        return {
            'status': 'success',
            'records': total,
            'duration': duration,
            'response': response_data,
        }

    except urllib.error.URLError as e:
        duration = round(time.time() - start_time, 2)
        reason = str(e.reason) if hasattr(e, 'reason') else str(e)
        logger.warning(f"❌ সিঙ্ক ব্যর্থ: {reason}")

        try:
            from apps.sync.models import SyncLog
            SyncLog.objects.create(
                status='failed',
                direction='push',
                error_message=reason,
                duration_seconds=duration,
            )
        except Exception:
            pass

        return {'status': 'failed', 'error': reason}

    except Exception as e:
        logger.error(f"❌ সিঙ্ক ত্রুটি: {e}")
        return {'status': 'failed', 'error': str(e)}


# ──────────────────────────────────────────────
#  ব্যাকগ্রাউন্ড সিঙ্ক ম্যানেজার ক্লাস
# ──────────────────────────────────────────────
class SyncManager:
    """
    ব্যাকগ্রাউন্ড থ্রেডে পর্যায়ক্রমে সিঙ্ক চালায়।
    launcher.py থেকে ব্যবহার করা হয়।
    """

    def __init__(self, interval_seconds=None):
        self.interval = interval_seconds or SYNC_INTERVAL_SECONDS
        self._stop_event = threading.Event()
        self._thread = None
        self.last_sync_result = None

    def start(self):
        """ব্যাকগ্রাউন্ড সিঙ্ক থ্রেড শুরু করে।"""
        if self._thread and self._thread.is_alive():
            logger.info("SyncManager ইতিমধ্যে চলছে।")
            return

        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._run_loop,
            name='SyncManager',
            daemon=True
        )
        self._thread.start()
        logger.info(f"🔄 SyncManager শুরু হয়েছে (প্রতি {self.interval // 60} মিনিটে)।")

    def stop(self):
        """সিঙ্ক থ্রেড বন্ধ করে।"""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)
        logger.info("⏹️ SyncManager বন্ধ হয়েছে।")

    def _run_loop(self):
        """মূল সিঙ্ক লুপ।"""
        # প্রথম রান ৩০ সেকেন্ড পরে (সার্ভার স্টার্ট হতে দেওয়া)
        logger.info("প্রথম সিঙ্কের জন্য ৩০ সেকেন্ড অপেক্ষা করছে...")
        if self._stop_event.wait(timeout=30):
            return

        while not self._stop_event.is_set():
            try:
                self.last_sync_result = run_sync_now()
            except Exception as e:
                logger.error(f"সিঙ্ক লুপ ত্রুটি: {e}")

            # পরবর্তী সিঙ্কের জন্য অপেক্ষা
            if self._stop_event.wait(timeout=self.interval):
                break

    def is_running(self):
        return self._thread is not None and self._thread.is_alive()

    def sync_now(self):
        """বাইরে থেকে তাৎক্ষণিক সিঙ্ক ট্রিগার করা।"""
        result = run_sync_now()
        self.last_sync_result = result
        return result


# ──────────────────────────────────────────────
#  CLI সাপোর্ট
# ──────────────────────────────────────────────
if __name__ == '__main__':
    print("📡 সিঙ্ক ম্যানেজার চলছে...")
    result = run_sync_now()
    print(f"ফলাফল: {json.dumps(result, ensure_ascii=False, indent=2)}")
