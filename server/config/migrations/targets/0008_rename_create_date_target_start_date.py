# Generated by Django 3.2.2 on 2022-07-22 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('targets', '0007_rename_start_date_target_create_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='target',
            old_name='create_date',
            new_name='start_date',
        ),
    ]
