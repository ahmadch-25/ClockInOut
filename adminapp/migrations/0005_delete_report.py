# Generated by Django 3.1.6 on 2021-09-24 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0004_remove_report_user_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Report',
        ),
    ]
