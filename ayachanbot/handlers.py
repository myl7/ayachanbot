import tempfile

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext

from .services.anime_image_searching import search_anime_image
from ayachanbot import error


def handle_start(update: Update, context: CallbackContext):
    text = '''\
Welcome! I can do these for you:
* Anime image searching by outer links
'''
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def handle_anime_image_searching(update: Update, context: CallbackContext):
    try:
        fids = set()
        photos = [
            fids.add(p.file_unique_id) or p
            for p in update.effective_message.photo if p.file_unique_id not in fids
        ]
        for photo in photos:
            with tempfile.TemporaryFile() as f:
                context.bot.get_file(photo.file_id).download(out=f)
                f.seek(0)
                res = search_anime_image(f)
                n = len(res.keys()) // 2
            text = 'Click the below buttons to view the results of different sources.'
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                reply_to_message_id=update.effective_message.message_id,
                text=text,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text=k, url=v) for k, v in list(res.items())[:n]],
                    [InlineKeyboardButton(text=k, url=v) for k, v in list(res.items())[n:]]
                ])
            )
    except error.AnimeImageSearchingError:
        text = 'Sorry, anime image searching is currently unavailable'
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)
