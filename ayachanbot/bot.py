import os
import logging

from telegram import Update
from telegram.ext import Updater, CallbackContext as Context, MessageHandler, Filters, Dispatcher

updater = Updater(token=os.getenv('BOT_TOKEN'), use_context=True)
dispatcher: Dispatcher = updater.dispatcher

logging.basicConfig(level=logging.INFO)


def pong(update: Update, context: Context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hello!')


pong_handler = MessageHandler(Filters.photo, pong)
dispatcher.add_handler(pong_handler)

updater.start_polling()
