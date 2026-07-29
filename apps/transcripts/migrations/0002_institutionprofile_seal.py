from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transcripts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='institutionprofile',
            name='seal',
            field=models.ImageField(blank=True, null=True, upload_to='seals/'),
        ),
    ]
