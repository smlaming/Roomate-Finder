# Generated by Django 3.1.6 on 2021-04-20 17:01

from django.db import migrations, models
import questionnaire.models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0005_auto_20210419_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='day',
            field=models.DateField(help_text='YYYY-MM-DD', validators=[questionnaire.models.day_validator]),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.TimeField(help_text='HH:MM', validators=[questionnaire.models.time_validator]),
        ),
    ]
