import os
from core import logger
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

from .commands import generate_menu, select_subreddit
from .handler import callback_handler

load_dotenv()


def run_bot():
    logger.info("Configuring bot")
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("stored", select_subreddit))    
    app.add_handler(CallbackQueryHandler(callback_handler))

    logger.info("Bot running.")
    app.run_polling()
