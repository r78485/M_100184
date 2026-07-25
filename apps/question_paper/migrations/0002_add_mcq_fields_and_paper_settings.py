from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('question_paper', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionbank',
            name='mcq_type',
            field=models.CharField(choices=[('SINGLE', 'সাধারণ বহুনির্বাচনী'), ('POLYNOMIAL', 'বহুপদী সমাপ্তিসূচক'), ('PASSAGE', 'উদ্দীপকভিত্তিক')], default='SINGLE', max_length=20),
        ),
        migrations.AddField(
            model_name='questionbank',
            name='statement_i',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='বিবৃতি i'),
        ),
        migrations.AddField(
            model_name='questionbank',
            name='statement_ii',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='বিবৃতি ii'),
        ),
        migrations.AddField(
            model_name='questionbank',
            name='statement_iii',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='বিবৃতি iii'),
        ),
        migrations.AddField(
            model_name='questionpaper',
            name='font_family',
            field=models.CharField(choices=[('ARIAL', 'English - Arial / Inter'), ('TIMES', 'English - Times New Roman'), ('ROBOTO', 'English - Roboto'), ('KALPURUSH', 'Bangla - Kalpurush'), ('SOLAIMANLIPI', 'Bangla - SolaimanLipi')], default='ARIAL', max_length=30),
        ),
        migrations.AddField(
            model_name='questionpaper',
            name='column_layout',
            field=models.CharField(choices=[('1', '1 Column (Full Width Standard)'), ('2', '2 Columns (NCTB Board Style)')], default='1', max_length=5),
        ),
        migrations.AddField(
            model_name='questionpaper',
            name='show_answer_key',
            field=models.BooleanField(default=False),
        ),
    ]
