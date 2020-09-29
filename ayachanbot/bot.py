import os
import logging
from io import BytesIO
import json
import yaml

from telegram import Update, Message, PhotoSize
from telegram.ext import Updater, CallbackContext as Context, MessageHandler, Filters, Dispatcher
import requests

updater = Updater(token=os.getenv('BOT_TOKEN'), use_context=True)
dispatcher: Dispatcher = updater.dispatcher

logging.basicConfig(level=logging.INFO)


def search_image(update: Update, context: Context):
    message: Message = update.effective_message
    photo_size: PhotoSize = message.photo[-1]
    photo = BytesIO()
    context.bot.get_file(photo_size.file_id).download(out=photo)
    photo.seek(0)
    results = search_on_saucenao(photo)
    result = results[0]
    text = yaml.dump(result['header'], indent=2, allow_unicode=True) \
           + '\n' + yaml.dump(result['data'], indent=2, allow_unicode=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text, reply_to_message_id=message.message_id)


def search_on_saucenao(file):
    resp = requests.post('https://saucenao.com/search.php', {
        'frame': 1,
        'hide': 0,
        'database': 999,
        'output_type': 2
    }, files={'file': file})
    results = json.loads(resp.content.decode())['results']
    return results


search_image_handler = MessageHandler(Filters.photo, search_image)
dispatcher.add_handler(search_image_handler)

updater.start_polling()
