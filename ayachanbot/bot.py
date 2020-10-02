import os
import logging

from telegram import Update, Message, PhotoSize
from telegram.ext import Updater, CallbackContext as Context, MessageHandler, Filters, Dispatcher

from .apis.saucenao import search_saucenao
from .apis.ascii2d import search_ascii2d
from .apis.whatanime import search_whatanime
from .report import Report

updater = Updater(token=os.getenv('BOT_TOKEN'), use_context=True)
dispatcher: Dispatcher = updater.dispatcher

logging.basicConfig(level=logging.INFO)


def search_image(update: Update, context: Context):
    message: Message = update.effective_message
    photo_size: PhotoSize = message.photo[-1]

    tmp_dir = '/tmp/ayachanbot/'
    filepath = tmp_dir + photo_size.file_id
    with open(filepath, 'wb') as f:
        context.bot.get_file(photo_size.file_id).download(out=f)

    saucenao_results = search_saucenao(filepath)
    ascii2d_results = search_ascii2d(filepath)
    whatanime_results = search_whatanime(filepath)

    report = Report() \
        .set_saucenao_results(saucenao_results) \
        .set_ascii2d_results(ascii2d_results) \
        .set_whatanime_results(whatanime_results) \
        .gen_report()
    context.bot.send_message(chat_id=update.effective_chat.id, text=report, reply_to_message_id=message.message_id)


search_image_handler = MessageHandler(Filters.photo, search_image)
dispatcher.add_handler(search_image_handler)

updater.start_polling()
updater.idle()
