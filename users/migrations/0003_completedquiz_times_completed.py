# Generated by Django 4.2 on 2024-03-14 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_completedquiz_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='completedquiz',
            name='times_completed',
            field=models.PositiveIntegerField(default=0),
        ),
    ]