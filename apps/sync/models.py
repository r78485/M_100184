from django.db import models
from django.utils import timezone


class SyncLog(models.Model):
    """লোকাল থেকে অনলাইনে সিঙ্কের লগ রেকর্ড।"""
    STATUS_CHOICES = [
        ('success', '✅ সফল'),
        ('failed', '❌ ব্যর্থ'),
        ('skipped', '⏭️ এড়িয়ে গেছে'),
        ('pending', '⏳ অপেক্ষায়'),
    ]

    synced_at = models.DateTimeField(default=timezone.now, verbose_name='সিঙ্কের সময়')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    direction = models.CharField(
        max_length=20,
        choices=[('push', 'লোকাল → অনলাইন'), ('pull', 'অনলাইন → লোকাল')],
        default='push'
    )
    records_synced = models.IntegerField(default=0, verbose_name='সিঙ্ক হওয়া রেকর্ড')
    error_message = models.TextField(blank=True, null=True, verbose_name='ত্রুটির বার্তা')
    duration_seconds = models.FloatField(default=0.0, verbose_name='সময় (সেকেন্ড)')

    class Meta:
        ordering = ['-synced_at']
        verbose_name = 'সিঙ্ক লগ'
        verbose_name_plural = 'সিঙ্ক লগগুলো'

    def __str__(self):
        return f"{self.get_direction_display()} | {self.get_status_display()} | {self.synced_at.strftime('%Y-%m-%d %H:%M')}"


class SyncConfig(models.Model):
    """সিঙ্ক কনফিগারেশন (একটিই সারি থাকবে)."""
    online_server_url = models.URLField(
        default='https://m-100184.onrender.com',
        verbose_name='অনলাইন সার্ভার URL'
    )
    api_key = models.CharField(
        max_length=128,
        default='',
        blank=True,
        verbose_name='API কী'
    )
    sync_interval_minutes = models.IntegerField(
        default=15,
        verbose_name='সিঙ্ক বিরতি (মিনিট)'
    )
    auto_sync_enabled = models.BooleanField(default=True, verbose_name='অটো-সিঙ্ক চালু')
    last_successful_sync = models.DateTimeField(null=True, blank=True, verbose_name='শেষ সফল সিঙ্ক')

    class Meta:
        verbose_name = 'সিঙ্ক কনফিগ'
        verbose_name_plural = 'সিঙ্ক কনফিগ'

    def __str__(self):
        return f"সিঙ্ক কনফিগ → {self.online_server_url}"

    @classmethod
    def get_config(cls):
        """সিঙ্গেলটন প্যাটার্নে কনফিগ নিয়ে আসে।"""
        config, _ = cls.objects.get_or_create(pk=1)
        return config
