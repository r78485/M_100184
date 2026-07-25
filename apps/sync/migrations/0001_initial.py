from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SyncConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('online_server_url', models.URLField(default='https://m-100184.onrender.com', verbose_name='অনলাইন সার্ভার URL')),
                ('api_key', models.CharField(blank=True, default='', max_length=128, verbose_name='API কী')),
                ('sync_interval_minutes', models.IntegerField(default=15, verbose_name='সিঙ্ক বিরতি (মিনিট)')),
                ('auto_sync_enabled', models.BooleanField(default=True, verbose_name='অটো-সিঙ্ক চালু')),
                ('last_successful_sync', models.DateTimeField(blank=True, null=True, verbose_name='শেষ সফল সিঙ্ক')),
            ],
            options={
                'verbose_name': 'সিঙ্ক কনফিগ',
                'verbose_name_plural': 'সিঙ্ক কনফিগ',
            },
        ),
        migrations.CreateModel(
            name='SyncLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('synced_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='সিঙ্কের সময়')),
                ('status', models.CharField(
                    choices=[('success', '✅ সফল'), ('failed', '❌ ব্যর্থ'), ('skipped', '⏭️ এড়িয়ে গেছে'), ('pending', '⏳ অপেক্ষায়')],
                    default='pending',
                    max_length=20,
                )),
                ('direction', models.CharField(
                    choices=[('push', 'লোকাল → অনলাইন'), ('pull', 'অনলাইন → লোকাল')],
                    default='push',
                    max_length=20,
                )),
                ('records_synced', models.IntegerField(default=0, verbose_name='সিঙ্ক হওয়া রেকর্ড')),
                ('error_message', models.TextField(blank=True, null=True, verbose_name='ত্রুটির বার্তা')),
                ('duration_seconds', models.FloatField(default=0.0, verbose_name='সময় (সেকেন্ড)')),
            ],
            options={
                'verbose_name': 'সিঙ্ক লগ',
                'verbose_name_plural': 'সিঙ্ক লগগুলো',
                'ordering': ['-synced_at'],
            },
        ),
    ]
