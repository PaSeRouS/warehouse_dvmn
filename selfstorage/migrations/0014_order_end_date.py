# Generated by Django 4.0.5 on 2022-07-05 12:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('selfstorage', '0013_order_name_alter_box_id_alter_customer_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='end_date',
            field=models.DateField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата окончания хранения'),
        ),
    ]
