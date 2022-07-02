# Generated by Django 3.1.14 on 2022-07-02 18:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('selfstorage', '0009_auto_20220702_2052'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='end_date',
        ),
        migrations.AddField(
            model_name='box',
            name='end_date',
            field=models.DateField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата окончания хранения'),
        ),
    ]
