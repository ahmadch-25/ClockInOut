# Generated by Django 3.1.6 on 2021-09-15 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0003_report'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='user_id',
        ),
    ]