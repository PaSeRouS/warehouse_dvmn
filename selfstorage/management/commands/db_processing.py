from datetime import date, datetime

from selfstorage.models import Box, Customer, Order
from selfstorage.models import Size, Warehouse


def create_customer (first_name: str,
                     last_name: str,
                     nickname: str,
                     phone_number: str,
                     patronymic='',
                     e_mail=''):

    Customer.objects.create(
        last_name=last_name,
        first_name=first_name,
        patronymic=patronymic,
        nickname=nickname,
        phone_number=phone_number,
        e_mail=e_mail
    )


def create_order (customer: Customer,
                  warehouse: Warehouse,
                  end_date: datetime.date,
                  box: Box,
                  price: int):

    name = f'Заказ №{len(Order.objects.all()) + 1}'

    Order.objects.create(
        name=name,
        customer=customer,
        warehouse=warehouse,
        box=box,
        price=price,
        end_date=end_date,
        paid=True)

    Box.objects.filter(
        name=box.name,
        warehouse=box.warehouse
    ).update(
        customer=customer,
        occupied=True,
        end_date=end_date
    )


def get_customer(nickname: str):
    customer = Customer.objects.get(
        nickname=nickname
    )

    return customer


def get_warehouse(address: str):
    warehouse = Warehouse.objects.get(
        address=address
    )

    return warehouse


def get_box(name: str, warehouse: Warehouse):
    box = Box.objects.get(
        name=name,
        warehouse=warehouse
    )

    return box


def get_free_boxes_from_warehouse(size: Size,
                                  floor: int, 
                                  warehouse: Warehouse):
    boxes = Box.objects.filter(
        size=size,
        floor=floor,
        warehouse=warehouse,
        occupied=False
    )

    return boxes


def get_sizes():
    return Size.objects.all()


def get_size(name: str):
    return Size.objects.get(
        name=name
    )


def get_customers_boxes(customer: Customer):
    return customer.boxes.all()


def get_customers_orders(customer: Customer):
    return customer.orders.all()


def get_warehouses():
    return Warehouse.objects.all()

def get_order(name: str):
    return Order.objects.select_related('box').get(
        name=name
    )