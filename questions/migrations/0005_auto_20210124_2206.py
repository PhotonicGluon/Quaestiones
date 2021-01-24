# Generated by Django 3.1.4 on 2021-01-24 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_question_question_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='num_players_solved',
            field=models.IntegerField(default=0, verbose_name='Number of players that solved this question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_slug',
            field=models.SlugField(help_text='This was automatically generated when the question is created.'),
        ),
    ]
