# Generated by Django 4.2 on 2024-03-14 02:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='completedquiz',
            options={'verbose_name': 'Competed Quiz', 'verbose_name_plural': 'Completed Quizes'},
        ),
        migrations.RenameField(
            model_name='completedquiz',
            old_name='score',
            new_name='max_score',
        ),
    ]
