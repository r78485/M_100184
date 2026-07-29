from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testimonials', '0004_student_roll_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institutionprofile',
            name='name_bn',
            field=models.CharField(default='গাজীমাহমুদ নিম্ন মাধ্যমিক বিদ্যালয়', max_length=255),
        ),
        migrations.AlterField(
            model_name='institutionprofile',
            name='name_en',
            field=models.CharField(default='Gazi Mahmud Secondary School', max_length=255),
        ),
    ]
