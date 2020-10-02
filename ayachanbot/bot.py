import os
import logging
from multiprocessing.dummy import Pool as ThreadPool

from telegram import Update, Message, PhotoSize
from telegram.ext import Updater, CallbackContext as Context, MessageHandler, Filters, Dispatcher

from .apis.saucenao import search_saucenao
from .apis.ascii2d import search_ascii2d
from .apis.whatanime import search_whatanime
from .reports import report_saucenao, report_ascii2d, report_whatanime

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

    def search(api, report):
        results = api(filepath)
        for t in report(results):
            reply(t)

    def reply(t):
        context.bot.send_message(chat_id=update.effective_chat.id, text=t, reply_to_message_id=message.message_id)

    with ThreadPool(3) as pool:
        pool.starmap(search, [
            (search_saucenao, report_saucenao),
            (search_ascii2d, report_ascii2d),
            (search_whatanime, report_whatanime)
        ])


search_image_handler = MessageHandler(Filters.photo, search_image)
dispatcher.add_handler(search_image_handler)

updater.start_polling()
updater.idle()
