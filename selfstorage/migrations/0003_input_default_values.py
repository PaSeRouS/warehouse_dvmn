from django.db import migrations
import random

def test_values(apps, schema_editor):
    Box = apps.get_model('selfstorage', 'Box')
    Size = apps.get_model('selfstorage', 'Size')
    Warehouse = apps.get_model('selfstorage', 'Warehouse')

    Size.objects.create(
        name='< 3 кг'
    )

    Size.objects.create(
        name='3-10 кг'
    )

    Size.objects.create(
        name='> 10 кг'
    )

    sizes = Size.objects.all()

    warehouse_names = [
        'Склад на улице Литвина-Седого',
        'Склад на улице Дальняя',
        'Склад на Чистопрудном бульваре',
        'Склад на Игорском проезде',
        'Склад на Цветочном проезде'
    ]

    addresses = [
        'г.Москва, ул.Литвина-Седого, д.7А',
        'г.Москва, ул.Дальняя, д.11',
        'г.Москва, Чистопрудный бульвар, д.12 с7',
        'г.Москва, Игорский проезд, д.7 с11',
        'г.Москва, Цветочный проезд, д.4 с3'
    ]

    for i in range(5):
        number_of_floors = random.randint(2, 5)
        boxes_per_floor = random.randint(5, 10)

        warehouse = Warehouse.objects.create(
            name=warehouse_names[i],
            address=addresses[i],
            number_of_floors=number_of_floors,
            boxes_per_floor=boxes_per_floor
        )

        box_number = 0

        for floor_numb in range(number_of_floors):
            for _ in range(boxes_per_floor):
                box_number += 1

                Box.objects.create(
                    name=f'Бокс №{box_number}',
                    warehouse=warehouse,
                    size=random.choice(sizes),
                    floor=floor_numb+1
                )

class Migration(migrations.Migration):

    dependencies = [
        ('selfstorage', '0002_auto_20220630_1642'),
    ]

    operations = [
        migrations.RunPython(test_values)
    ]