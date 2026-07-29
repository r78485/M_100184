from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admit_cards', '0002_schoolprofile_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolprofile',
            name='seal',
            field=models.ImageField(blank=True, null=True, upload_to='seals/', verbose_name='প্রতিষ্ঠানের সিল (Round Seal)'),
        ),
    ]
