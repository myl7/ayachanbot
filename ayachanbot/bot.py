import os
import logging

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from . import handlers


def main():
    load_dotenv()
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    token = os.getenv('BOT_TOKEN')
    updater = Updater(token=token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', handlers.handle_start)
    dispatcher.add_handler(start_handler)

    anime_image_searching_handler = MessageHandler(
        Filters.photo & Filters.caption(['anime']),
        handlers.handle_anime_image_searching
    )
    dispatcher.add_handler(anime_image_searching_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()
