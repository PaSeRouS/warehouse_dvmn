from django.core.management.base import BaseCommand
from environs import Env
import telegram
from telegram.ext import (ConversationHandler, CommandHandler, Filters,
                          MessageHandler, Updater)
from .db_processing import (create_customer, create_order, get_customer,
                            get_warehouse, get_box,
                            get_free_boxes_from_warehouse)
from django.core.exceptions import ObjectDoesNotExist

(
    CREATE_ORDER,
    MY_ORDERS,
    FIRST_NAME,
    LAST_NAME,
    PATRONIC,
    PHONE,
    FINISH_REGISTRATION,
    USER_CHOICE,
    CHECK_CHOICE,
    NAME
    ) = range(10)


def start(update, context):
    custom_keyboard = [
        ['Создать заказ'], #
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
    except ObjectDoesNotExist:
        update.message.reply_text(start_message_new_user)
    return CHECK_CHOICE


def check_user_input(update, context):
    user_input = update.message.text
    if 'Да'.lower() == user_input:
        update.message.reply_text(
            'Укажите свой email',
            reply_markup=telegram.ReplyKeyboardRemove(),
            )
        return PHONE
    else:
        update.message.reply_text(
            'Для регистрации в сервисе нужно принять согласие '
            'на обработку персональных данных. \nДо новых встреч!',
            reply_markup=telegram.ReplyKeyboardRemove(),
            )
        return ConversationHandler.END


def phone(update, context):
    update.message.reply_text('Укажите свой телефон в формате +7')
    context.user_data["email"] = update.message.text
    return FIRST_NAME


def first_name(update, context):
    update.message.reply_text('Укажите свое имя')
    context.user_data["phone"] = update.message.text
    return LAST_NAME


def last_name(update, context):
    update.message.reply_text('Укажите свою фамилию')
    context.user_data["first_name"] = update.message.text
    return PATRONIC


def patronic(update, context):
    update.message.reply_text('Укажите свое отчество')
    context.user_data["last_name"] = update.message.text
    return FINISH_REGISTRATION


def finish_registration(update, context):
    context.user_data["patronic"] = update.message.text
    update.message.reply_text('Регистрация успешно завершена!')
    update.message.reply_text('Ваши данные:{}'.format(context.user_data))
    nickname = update.message.chat.username
    create_customer(context.user_data["first_name"],
                    context.user_data["last_name"],
                    nickname,
                    context.user_data["phone"],
                    patronymic=context.user_data["patronic"],
                    e_mail=context.user_data["email"])
    return ConversationHandler.END


def handle_create_order(update, context):
    pass


def handle_orders(update, context):
    pass


def stop(update, context):
    update.message.reply_text(
        'Спасибо что вы с нами!',
        reply_markup=telegram.ReplyKeyboardRemove()
        )
    return ConversationHandler.END


class Command(BaseCommand):
    help = "Telegram bot"

    def handle(self, *args, **kwargs):
        env = Env()
        env.read_env()
        telegram_bot_token = env.str("TELEGRAM_BOT_TOKEN")
        updater = Updater(telegram_bot_token)
        dispatcher = updater.dispatcher
        conv_handler = ConversationHandler(
            entry_points=[
                CommandHandler('start', start),
                ],
            states={
                CREATE_ORDER: [
                    MessageHandler(
                        Filters.regex('^Создать заказ'),
                        handle_create_order,
                        ),
                    ],
                MY_ORDERS: [
                    MessageHandler(Filters.regex('^Мои заказы'), handle_orders),
                    ],
                CHECK_CHOICE: [MessageHandler(Filters.text, check_user_input)],
                PHONE: [MessageHandler(Filters.text, phone)],
                FIRST_NAME: [MessageHandler(Filters.text, first_name)],
                LAST_NAME: [MessageHandler(Filters.text, last_name)],
                PATRONIC: [MessageHandler(Filters.text, patronic)],
                FINISH_REGISTRATION: [MessageHandler(
                    Filters.text,
                    finish_registration,
                    )]
            },
            fallbacks=[CommandHandler('stop', stop)],
        )
        dispatcher.add_handler(conv_handler)
        updater.start_polling()
        updater.idle()
