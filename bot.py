from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from data import db_session


def echo(update, context):
    update.message.reply_text(f'Я получил сообщение {update.message.text}')


reply_keyboard = [['/help', '/site'],
                  ['/site']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def main():
    updater = Updater("1797783540:AAFPXzqG6tbfgAWPPF6tQ0j05X7UJ10iAqE", use_context=True)
    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(text_handler)
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("site", site))
    dp.add_handler(CommandHandler("close", close_keyboard))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), date))
    updater.start_polling()
    updater.idle()


def close_keyboard(update, context):
    update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove())


def help(update, context):
    update.message.reply_text(
        "Я бот, отправьте мне даты заезда и выезда через пробел,"
        " и я вам выведу количество свободных номеров")


def site(update, context):
    update.message.reply_text("Сайт: http://127.0.0.1:5000/booking/")


def date(update, context):



if __name__ == '__main__':
    main()
