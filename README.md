# SelfStorage

Сервис для бронирования боксов для хранения вещей на складах Москвы.
После регистрации в боте сервис позволяет оформить заказ на хранение или посмотреть уже сделланые пользователем заказы.

Заказ осуществляется с помощью выбора последовательныъ опций, в которые входят склад, размер бокса и номер этажа склада, на котором располагается бокс.
После введения параметров пользователю будет выдан пеечнь доступных боксов, из которых он может выбрать подходящий бокс. Затем нужно ввести количество месяцев для хранения и оплатить заказ.

## Установка приложения
Склонируйте репозиторий, активируйте виртуальное пространство, сделайте миграции и создайте суперпользователя.

```
git clone https://github.com/PaSeRouS/warehouse_dvmn
cd warehouse_dvmn
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
python3 manage.py migrate && python3 manage.py createsuperuser
```

Создайте файл .env и запишите в него все нужные данные:
```
TELEGRAM_BOT_TOKEN=Токен вашего бота в телеграме, который выдаёт @BotFather (Пример: 1234567890:ABCDEFGHIjklmnoPqrsStuvwxyzINet1234)
PAYMENTS_PROVIDER_TOKEN=Токен для оплаты от телеграм бота @BotFather (Пример: 12345678912376543:TEST:123456)
DJANGO_SECRET_KEY=Секретный ключ проекта Django (Пример: qpr$_gl&n-8x5n934hmopzgh+$eu)#j^m#(z+il1lzfskzzbzu)
```

[Инструкция](https://core.telegram.org/bots/payments#getting-a-token) для получени токена для платежей.

### Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).