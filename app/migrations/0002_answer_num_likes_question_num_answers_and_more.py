# Generated by Django 5.0.4 on 2024-04-10 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='num_likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='num_answers',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='num_likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tag',
            name='num_questions',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user_profile',
            name='activity',
            field=models.IntegerField(default=0),
        ),
    ]