# Generated by Django 3.1.4 on 2020-12-31 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_profile_solved_puzzles'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='puzzles_solved',
        ),
    ]
