from datetime import date

import telegram
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from environs import Env
from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)

from .db_processing import (create_customer, create_order, get_box,
                            get_customer, get_free_boxes_from_warehouse,
                            get_size, get_sizes, get_warehouse, get_warehouses)

(
    FIRST_NAME,
    LAST_NAME,
    PATRONIC,
    PHONE,
    FINISH_REGISTRATION,
    USER_CHOICE,
    CHECK_CHOICE_NEW_USER,
    CHECK_CHOICE_EXIST_USER,
    SIZE,
    FLOOR,
    FREE_BOX,
    ORDER,
    STORAGE_PERIOD,
    ) = range(13)


def start(update, context):
    custom_keyboard = [
        ['Заказать бокс'],
        ['Мои заказы'],
        ]
    reply_markup = telegram.ReplyKeyboardMarkup(
        custom_keyboard
        )
    start_message_new_user = 'Здравствуйте! '\
        'Я бот компании Сервис SelfStorage!\n'\
        'У нас вы можете разместить '\
        'и хранить свои вещи в целости и сохранности.\n'\
        'Похоже, что вы еще не пользовались нашими услугами и хотели бы  '\
        'заказать хранение. Для этого вам необходимо зарегистрироваться.\n'\
        'Вы согласны на обработку персональных данных, '\
        'для регистрирации в нашем сервисе?'
    start_message_exist_user = 'Здравствуйте! '\
        'Я бот компании Сервис SelfStorage!\n'\
        'У нас вы можете разместить '\
        'и хранить свои вещи в целости и сохранности.\n'\
        'Чем могу вам помочь ?  '
    nickname = update.message.chat.username
    try:
        get_customer(nickname)
        update.message.reply_text(
            start_message_exist_user,
            reply_markup=reply_markup,
            )
        return CHECK_CHOICE_EXIST_USER
    except ObjectDoesNotExist:
        update.message.reply_text(start_message_new_user)
        return CHECK_CHOICE_NEW_USER


def check_new_user_input(update, context):
    user_input = update.message.text
    if 'Да'.lower() == user_input:
        update.message.reply_text(
            'Укажите свой email',
            reply_markup=telegram.ReplyKeyboardRemove(),
            )
        state = PHONE
    else:
        update.message.reply_text(
            'Для регистрации в сервисе нужно принять согласие '
            'на обработку персональных данных. \nДо новых встреч!',
            reply_markup=telegram.ReplyKeyboardRemove(),
            )
        state = ConversationHandler.END
    return state


def check_exist_user_input(update, context):
    user_input = update.message.text
    if 'Заказать бокс' == user_input:
        warehouses = get_warehouses()
        warehouses_adresses = [warehouse.address for warehouse in warehouses]
        custom_keyboard = [[address] for address in warehouses_adresses]
        reply_markup = telegram.ReplyKeyboardMarkup(
            custom_keyboard,
        )
        update.message.reply_text(
                'Выберите адрес склада',
                reply_markup=reply_markup,
                )
        return SIZE


def size(update, context):
    warehouse = get_warehouse(update.message.text)
    context.user_data['warehouse'] = warehouse
    sizes = get_sizes()
    custom_keyboard = [[size.name] for size in sizes]
    reply_markup = telegram.ReplyKeyboardMarkup(
        custom_keyboard,
    )
    update.message.reply_text(
            'Выберите размер бокса',
            reply_markup=reply_markup,
            )
    return FLOOR


def floor(update, context):
    context.user_data['size'] = get_size(update.message.text)
    number_of_floors = context.user_data['warehouse'].number_of_floors
    custom_keyboard = [
        [floor_num] for floor_num in range(1, number_of_floors+1)
        ]
    reply_markup = telegram.ReplyKeyboardMarkup(
        custom_keyboard,
    )
    update.message.reply_text(
            'Выберите этаж',
            reply_markup=reply_markup,
            )
    return FREE_BOX


def free_box(update, context):
    context.user_data['floor'] = update.message.text
    free_boxes = get_free_boxes_from_warehouse(
        context.user_data['size'],
        context.user_data['floor'],
        context.user_data['warehouse'],
    )
    custom_keyboard = [[box.name] for box in free_boxes]
    reply_markup = telegram.ReplyKeyboardMarkup(
        custom_keyboard,
    )
    update.message.reply_text(
            'Мы можем предложить вам следующие боксы',
            reply_markup=reply_markup,
            )
    return STORAGE_PERIOD


def storage_period(update, context):
    context.user_data['box'] = get_box(
         update.message.text,
         context.user_data['warehouse'],
         )
    update.message.reply_text(
            'Укажите срок хранения в месяцах',
            reply_markup=telegram.ReplyKeyboardRemove(),
            )
    return ORDER


def order(update, context):
    nickname = update.message.chat.username
    customer = get_customer(nickname)
    storage_period = update.message.text
    end_date = date.today() + relativedelta(months=+int(storage_period))
    context.user_data['end_date'] = end_date
    price = 199
    create_order(
        customer,
        context.user_data['warehouse'],
        end_date,
        context.user_data['box'],
        price,
        )
    update.message.reply_text(
        'Благодарим вас за заказ! Привозите свои вещи по адресу: {}\n'
        'Этаж № {}\n{}\n'
        'Ваши вещи будут храниться до {}'.format(
            context.user_data['warehouse'].address,
            context.user_data['floor'],
            context.user_data['box'].name,
            end_date,
            )
        )
    return ConversationHandler.END


def phone(update, context):
    update.message.reply_text('Укажите свой телефон в формате +7')
    context.user_data['email'] = update.message.text
    return FIRST_NAME


def first_name(update, context):
    update.message.reply_text('Укажите свое имя')
    context.user_data['phone'] = update.message.text
    return LAST_NAME


def last_name(update, context):
    update.message.reply_text('Укажите свою фамилию')
    context.user_data['first_name'] = update.message.text
    return PATRONIC


def patronic(update, context):
    update.message.reply_text('Укажите свое отчество')
    context.user_data['last_name'] = update.message.text
    return FINISH_REGISTRATION


def finish_registration(update, context):
    context.user_data['patronic'] = update.message.text
    update.message.reply_text('Регистрация успешно завершена!')
    nickname = update.message.chat.username
    create_customer(context.user_data['first_name'],
                    context.user_data['last_name'],
                    nickname,
                    context.user_data['phone'],
                    patronymic=context.user_data['patronic'],
                    e_mail=context.user_data['email'])
    return ConversationHandler.END


def stop(update, context):
    update.message.reply_text(
        'До скорых встреч!',
        reply_markup=telegram.ReplyKeyboardRemove()
        )
    return ConversationHandler.END


class Command(BaseCommand):
    help = 'Telegram bot'

    def handle(self, *args, **kwargs):
        env = Env()
        env.read_env()
        telegram_bot_token = env.str('TELEGRAM_BOT_TOKEN')
        updater = Updater(telegram_bot_token)
        dispatcher = updater.dispatcher
        conv_handler = ConversationHandler(
            entry_points=[
                CommandHandler('start', start),
                ],
            states={
                CHECK_CHOICE_NEW_USER: [MessageHandler(
                    Filters.text & (~ Filters.command),
                    check_new_user_input,
                    )],
                CHECK_CHOICE_EXIST_USER: [MessageHandler(
                    Filters.text & (~ Filters.command),
                    check_exist_user_input,
                    )],
                PHONE: [MessageHandler(
                    Filters.text & (~ Filters.command),
                    phone,
                    )],
                FIRST_NAME: [
                    MessageHandler(
                        Filters.text & (~ Filters.command),
                        first_name,
                        )
                    ],
                LAST_NAME: [MessageHandler(
                    Filters.text & (~ Filters.command),
                    last_name,
                    )],
                PATRONIC: [MessageHandler(
                    Filters.text & (~ Filters.command),
                    patronic,
                    )],
                SIZE: [MessageHandler(
                    Filters.text & (~ Filters.command),
                    size,
                    )],
                FLOOR: [MessageHandler(
                    Filters.text & (~ Filters.command),
                    floor,
                    )],
                FREE_BOX: [MessageHandler(
                    Filters.text & (~ Filters.command),
                    free_box,
                    )],
                ORDER: [MessageHandler(
                    Filters.text & (~ Filters.command),
                    order,
                    )],
                STORAGE_PERIOD: [MessageHandler(
                    Filters.text & (~ Filters.command),
                    storage_period,
                    )],
                FINISH_REGISTRATION: [MessageHandler(
                    Filters.text & (~ Filters.command),
                    finish_registration,
                    )]
            },
            fallbacks=[CommandHandler('stop', stop)],
        )
        dispatcher.add_handler(conv_handler)
        updater.start_polling()
        updater.idle()
