import json
import time
import hashlib
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
from django.core import serializers
from django.db import transaction

from .models import SyncLog, SyncConfig

logger = logging.getLogger(__name__)


def get_sync_api_key():
    """Settings বা DB থেকে API কী নেওয়া।"""
    return getattr(settings, 'SYNC_API_KEY', 'offline-sync-secret-key-change-me')


def verify_api_key(request):
    """Request header থেকে API কী যাচাই।"""
    provided_key = request.headers.get('X-Sync-API-Key', '')
    return provided_key == get_sync_api_key()


# ────────────────────────────────────────────────────────────
#  Status API — অনলাইন/অফলাইন চেক করতে
# ────────────────────────────────────────────────────────────
def sync_status_api(request):
    """ড্যাশবোর্ডের AJAX কলের জন্য সিঙ্ক স্ট্যাটাস।"""
    try:
        cfg = SyncConfig.get_config()
        last_log = SyncLog.objects.filter(status='success').first()
        pending_count = SyncLog.objects.filter(status='pending').count()

        return JsonResponse({
            'online_server': cfg.online_server_url,
            'auto_sync': cfg.auto_sync_enabled,
            'sync_interval': cfg.sync_interval_minutes,
            'last_sync': last_log.synced_at.isoformat() if last_log else None,
            'last_sync_records': last_log.records_synced if last_log else 0,
            'pending_syncs': pending_count,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ────────────────────────────────────────────────────────────
#  Push API — লোকাল → অনলাইন (অনলাইন সার্ভার এই endpoint গ্রহণ করে)
# ────────────────────────────────────────────────────────────
@csrf_exempt
@require_http_methods(["POST"])
def sync_receive_push(request):
    """
    অনলাইন সার্ভারে এই endpoint-এ লোকাল ডেটা পাঠানো হয়।
    POST /api/sync/push/
    Header: X-Sync-API-Key: <key>
    Body: JSON with model data
    """
    if not verify_api_key(request):
        return JsonResponse({'error': 'Invalid API Key'}, status=403)

    start = time.time()
    log = SyncLog.objects.create(direction='pull', status='pending')

    try:
        payload = json.loads(request.body)
        models_data = payload.get('models', {})
        total_records = 0

        with transaction.atomic():
            for model_name, objects_json in models_data.items():
                try:
                    for obj in serializers.deserialize('json', json.dumps(objects_json)):
                        obj.save()
                        total_records += 1
                except Exception as model_err:
                    logger.warning(f"Model {model_name} sync error: {model_err}")

        log.status = 'success'
        log.records_synced = total_records
        log.duration_seconds = time.time() - start
        log.save()

        return JsonResponse({
            'status': 'ok',
            'records_received': total_records,
            'duration': log.duration_seconds,
        })

    except Exception as e:
        log.status = 'failed'
        log.error_message = str(e)
        log.duration_seconds = time.time() - start
        log.save()
        logger.error(f"Sync push receive error: {e}")
        return JsonResponse({'error': str(e)}, status=500)


# ────────────────────────────────────────────────────────────
#  Pull API — অনলাইন → লোকাল (লোকাল এখান থেকে ডেটা নামাবে)
# ────────────────────────────────────────────────────────────
@csrf_exempt
@require_http_methods(["GET"])
def sync_export_data(request):
    """
    অনলাইন সার্ভার থেকে ডেটা রপ্তানি করার endpoint।
    লোকাল এখানে GET করে ডেটা নামাবে।
    GET /api/sync/export/
    Header: X-Sync-API-Key: <key>
    """
    if not verify_api_key(request):
        return JsonResponse({'error': 'Invalid API Key'}, status=403)

    try:
        from apps.users.models import User, Student, Teacher, Employee, SchoolSettings
        from apps.academics.models import Class, Section, Subject

        export = {}

        # Students
        students = Student.objects.all()
        export['students'] = json.loads(serializers.serialize('json', students))

        # Classes
        try:
            classes = Class.objects.all()
            export['classes'] = json.loads(serializers.serialize('json', classes))
        except Exception:
            export['classes'] = []

        # Subjects
        try:
            subjects = Subject.objects.all()
            export['subjects'] = json.loads(serializers.serialize('json', subjects))
        except Exception:
            export['subjects'] = []

        total = sum(len(v) for v in export.values())

        return JsonResponse({
            'status': 'ok',
            'exported_at': timezone.now().isoformat(),
            'total_records': total,
            'models': export,
        })

    except Exception as e:
        logger.error(f"Sync export error: {e}")
        return JsonResponse({'error': str(e)}, status=500)


# ────────────────────────────────────────────────────────────
#  Manual Sync Trigger (ড্যাশবোর্ড থেকে)
# ────────────────────────────────────────────────────────────
@login_required
@require_http_methods(["POST"])
def trigger_manual_sync(request):
    """অ্যাডমিন ড্যাশবোর্ড থেকে ম্যানুয়ালি সিঙ্ক শুরু করা।"""
    try:
        from sync_manager import run_sync_now
        result = run_sync_now()
        return JsonResponse({'status': 'ok', 'result': result})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
