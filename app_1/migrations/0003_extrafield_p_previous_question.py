# Generated by Django 4.1.7 on 2023-02-17 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0002_rename_p_id_submission_player'),
    ]

    operations = [
        migrations.AddField(
            model_name='extrafield',
            name='p_previous_question',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
