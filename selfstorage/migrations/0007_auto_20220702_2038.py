# Generated by Django 3.1.14 on 2022-07-02 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('selfstorage', '0006_auto_20220702_2033'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='pure_phone',
            new_name='phone_number',
        ),
    ]
