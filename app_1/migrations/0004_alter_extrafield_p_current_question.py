# Generated by Django 4.1.7 on 2023-02-17 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0003_extrafield_p_previous_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extrafield',
            name='p_current_question',
            field=models.IntegerField(blank=True, default=1),
        ),
    ]
