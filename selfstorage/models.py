from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

class Warehouse(models.Model):
    name = models.CharField(
        'Название склада',
        max_length=30,
        help_text='Склад на Арбате'
    )

    address = models.TextField(
        'Адрес склада',
        help_text='г.Москва, ул.Подольских курсантов, д.5'
    )

    number_of_floors = models.IntegerField(
        'Количество этажей',
        help_text='3'
    )

    boxes_per_floor = models.IntegerField(
        'Количество боксов на этаже',
        help_text='3')

    def __str__(self):
        return f'{self.name} ({self.address})'


class Order(models.Model):
    customer = models.ForeignKey(
        'Customer',
        verbose_name='Покупатель',
        related_name='orders',
        on_delete=models.CASCADE,
        db_index=True
    )

    warehouse = models.ForeignKey(
        'Warehouse',
        verbose_name='Склад',
        related_name='orders',
        on_delete=models.PROTECT)

    box = models.ForeignKey(
        'Box',
        verbose_name='Бокс',
        related_name='orders',
        on_delete=models.PROTECT
    )

    price = models.IntegerField(
        'Стоимость заказа',
        db_index=True,
    )

    paid = models.BooleanField(
        'Оплачен', 
        db_index=True, 
        default=False
    )

    created_at = models.DateTimeField(
        'Дата создания заказа',
        default=timezone.now,
        db_index=True)

    def __str__(self):
        return f'{self.customer}, {self.warehouse}'


class Customer(models.Model):
    last_name = models.CharField(
        'Фамилия',
        max_length=20
    )
    
    first_name = models.CharField(
        'Имя',
        max_length=20
    )
    
    patronymic = models.CharField(
        'Отчество',
        max_length=20,
        null=True,
        blank=True
    )

    nickname = models.CharField(
        'Никнейм в телеграме',
        max_length=30,
        db_index=True,
        default='@WarehouseDevman_bot'
    )

    phone_number = PhoneNumberField(
        'Номер телефона'
    )

    e_mail = models.CharField(
        'E-mail адрес',
        max_length=30,
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic}'


class Box(models.Model):
    name = models.CharField(
        'Название бокса',
        max_length=20,
        help_text='Бокс №1'
    )

    warehouse = models.ForeignKey(
        'Warehouse',
        verbose_name='Склад',
        related_name='boxes',
        on_delete=models.CASCADE
    )

    size = models.ForeignKey(
        'Size',
        verbose_name='Объём бокса',
        related_name='boxes',
        on_delete=models.PROTECT
    )

    floor = models.IntegerField(
        'Номер этажа',
        help_text='3')

    occupied = models.BooleanField(
        'Занят', 
        db_index=True, 
        default=False
    )

    customer = models.ForeignKey(
        'Customer',
        verbose_name='Кем занят',
        related_name='boxes',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    end_date = models.DateField(
        'Дата окончания хранения',
        default=timezone.now,
        db_index=True
    )

    def __str__(self):
        return f'{self.name}, {self.size}, {self.warehouse.name}'


class Size(models.Model):
    name = models.CharField(
        'Наименование размера',
        max_length=20,
        help_text='3 кг, 3-10кг'
    )

    def __str__(self):
        return self.name