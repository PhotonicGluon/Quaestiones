# Generated by Django 3.1.4 on 2021-01-11 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210111_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='possible_new_email',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]
