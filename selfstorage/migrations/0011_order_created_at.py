# Generated by Django 3.1.14 on 2022-07-02 18:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('selfstorage', '0010_auto_20220702_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата создания заказа'),
        ),
    ]
