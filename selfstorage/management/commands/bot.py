from django.core.management.base import BaseCommand
from environs import Env
import telegram
from telegram.ext import (ConversationHandler, CommandHandler, Filters,
                          MessageHandler, Updater)

(
    CREATE_ORDER,
    MY_ORDERS,
    NAME,
    PHONE,
    FINISH_REGISTRATION,
    USER_CHOICE,
    CHECK_CHOICE
    ) = range(7)


def start(update, context):
    custom_keyboard = [
        ['Создать заказ'],
        ['Зарегистрироваться'],
        ['Мои заказы'],
        ]
    reply_markup = telegram.ReplyKeyboardMarkup(
        custom_keyboard
        )
    start_message = 'Здравствуйте! Я бот компании Складмэн!\n'\
        'У нас вы можете разместить '\
        'и хранить свои вещи в целости и сохранности.\n'\
        'Если вы еще не пользовались нашими услугами и хотели бы заказать '\
        'хранение, нажмите «Зарегистрироваться».'
    update.message.reply_text(start_message, reply_markup=reply_markup)
    return CHECK_CHOICE

# TODO Согласие на обработку перс. данных


def check_user_input(update, context):
    user_input = update.message.text
    if "Зарегистрироваться" in user_input:
        update.message.reply_text(
            'Укажите свой email',
            reply_markup=telegram.ReplyKeyboardRemove(),
            )
        return PHONE


def phone(update, context):
    update.message.reply_text('Укажите свой телефон в формате +7')
    context.user_data["email"] = update.message.text
    return NAME


def name(update, context):
    update.message.reply_text('Укажите свою фамилию и имя')
    context.user_data["phone"] = update.message.text
    return FINISH_REGISTRATION


def finish_registration(update, context):
    context.user_data["name"] = update.message.text
    update.message.reply_text('Регистрация успешно завершена!')
    update.message.reply_text('Ваши данные:{}'.format(context.user_data))
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
                NAME: [MessageHandler(Filters.text, name)],
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
