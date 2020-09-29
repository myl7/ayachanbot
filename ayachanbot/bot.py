import os
import logging
from io import BytesIO

from telegram import Update, Message, PhotoSize
from telegram.ext import Updater, CallbackContext as Context, MessageHandler, Filters, Dispatcher

from .source import search_saucenao
from .report import Report

updater = Updater(token=os.getenv('BOT_TOKEN'), use_context=True)
dispatcher: Dispatcher = updater.dispatcher

logging.basicConfig(level=logging.INFO)


def search_image(update: Update, context: Context):
    message: Message = update.effective_message
    photo_size: PhotoSize = message.photo[-1]
    photo = BytesIO()
    context.bot.get_file(photo_size.file_id).download(out=photo)

    photo.seek(0)
    saucenao_results = search_saucenao(photo)

    texts = Report().set_saucenao_results(saucenao_results).gen_report()
    for text in texts:
        context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_to_message_id=message.message_id)


search_image_handler = MessageHandler(Filters.photo, search_image)
dispatcher.add_handler(search_image_handler)

updater.start_polling()
