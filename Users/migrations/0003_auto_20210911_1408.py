# Generated by Django 3.1.6 on 2021-09-11 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_auto_20210911_1358'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Employee',
            new_name='User',
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
    ]