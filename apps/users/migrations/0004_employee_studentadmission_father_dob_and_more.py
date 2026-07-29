from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_studentadmission_address_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_id', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('role', models.CharField(blank=True, default='Staff', max_length=100)),
                ('dept', models.CharField(blank=True, default='General', max_length=100)),
                ('email', models.CharField(blank=True, default='', max_length=150)),
                ('join_date', models.CharField(blank=True, default='', max_length=50)),
                ('active', models.BooleanField(default=True)),
                ('username', models.CharField(blank=True, default='', max_length=100)),
                ('pass_val', models.CharField(blank=True, default='12345', max_length=100)),
                ('father_name', models.CharField(blank=True, default='', max_length=200)),
                ('mother_name', models.CharField(blank=True, default='', max_length=200)),
                ('spouse_name', models.CharField(blank=True, default='', max_length=200)),
                ('dob', models.CharField(blank=True, default='', max_length=50)),
                ('gender', models.CharField(blank=True, default='Male', max_length=20)),
                ('blood', models.CharField(blank=True, default='A+', max_length=10)),
                ('religion', models.CharField(blank=True, default='Islam', max_length=50)),
                ('nid', models.CharField(blank=True, default='', max_length=50)),
                ('index_no', models.CharField(blank=True, default='', max_length=50)),
                ('appointment_date', models.CharField(blank=True, default='', max_length=50)),
                ('first_mpo', models.CharField(blank=True, default='', max_length=50)),
                ('pay_code', models.CharField(blank=True, default='20', max_length=20)),
                ('primary_phone', models.CharField(blank=True, default='', max_length=30)),
                ('present_addr', models.TextField(blank=True, default='')),
                ('edu', models.CharField(blank=True, default='', max_length=200)),
                ('exp', models.CharField(blank=True, default='', max_length=100)),
                ('basic_salary', models.CharField(blank=True, default='12,000', max_length=50)),
                ('photo', models.TextField(blank=True, default='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='studentadmission',
            name='father_dob',
            field=models.DateField(blank=True, null=True, verbose_name='পিতার জন্ম তারিখ / Father DOB'),
        ),
        migrations.AddField(
            model_name='studentadmission',
            name='father_occupation',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='পিতার পেশা / Father Occupation'),
        ),
        migrations.AddField(
            model_name='studentadmission',
            name='mother_dob',
            field=models.DateField(blank=True, null=True, verbose_name='মাতার জন্ম তারিখ / Mother DOB'),
        ),
        migrations.AddField(
            model_name='studentadmission',
            name='mother_occupation',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='মাতার পেশা / Mother Occupation'),
        ),
        migrations.AddField(
            model_name='studentadmission',
            name='permanent_post_office',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='ডাকঘর / Post Office'),
        ),
        migrations.AddField(
            model_name='studentadmission',
            name='present_post_office',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='ডাকঘর / Post Office'),
        ),
    ]
