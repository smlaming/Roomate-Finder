# Generated by Django 3.1.5 on 2021-04-02 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0008_auto_20210402_1303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='user',
        ),
    ]