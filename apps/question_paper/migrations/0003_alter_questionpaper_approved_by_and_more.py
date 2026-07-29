from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question_paper', '0002_add_mcq_fields_and_paper_settings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionbank',
            name='stimulus_table_data',
            field=models.JSONField(blank=True, help_text='Table or graph configuration', null=True),
        ),
        migrations.AlterField(
            model_name='questionpaper',
            name='approved_by',
            field=models.CharField(default='Headmaster', max_length=100),
        ),
        migrations.AlterField(
            model_name='questionpaper',
            name='column_layout',
            field=models.CharField(choices=[('1', '1 Column (Full Width Standard)'), ('2', '2 Columns (NCTB Board Exam Style)')], default='1', max_length=5),
        ),
        migrations.AlterField(
            model_name='questionpaper',
            name='instructions',
            field=models.TextField(default='1. Figures to the right indicate full marks.\n2. Read questions carefully before answering.\n3. Calculator is allowed where necessary.'),
        ),
        migrations.AlterField(
            model_name='questionpaper',
            name='numbering_style',
            field=models.CharField(choices=[('BANGLA', 'Bangla (১, ২, ৩ / ক, খ, গ)'), ('ENGLISH', 'English (1, 2, 3 / a, b, c)'), ('ROMAN', 'Roman (i, ii, iii)')], default='ENGLISH', max_length=20),
        ),
        migrations.AlterField(
            model_name='questionpaper',
            name='prepared_by',
            field=models.CharField(default='Subject Teacher', max_length=100),
        ),
        migrations.AlterField(
            model_name='questionpaper',
            name='school_name',
            field=models.CharField(default='Gazimahmud Secondary School', max_length=255),
        ),
        migrations.AlterField(
            model_name='questionpaper',
            name='subject',
            field=models.CharField(default='Mathematics', max_length=50),
        ),
        migrations.AlterField(
            model_name='questionpaper',
            name='time_allowed',
            field=models.CharField(default='3 Hours', max_length=100, verbose_name='পরীক্ষার সময়'),
        ),
        migrations.AlterField(
            model_name='questionpaper',
            name='title',
            field=models.CharField(default='Annual Examination — 2026', max_length=255, verbose_name='প্রশ্নপত্রের শিরোনাম / Exam Name'),
        ),
        migrations.AlterField(
            model_name='questionpaper',
            name='verified_by',
            field=models.CharField(default='Exam Controller', max_length=100),
        ),
    ]
