from core import logger

from telegram import (
    Update,    
    InlineKeyboardMarkup,
)

from .utils import _btn, _p, Command


async def generate_menu(update: Update, _):
    logger.info(f"User {update.effective_user.id} started the bot.")
    options = [
        [_btn("From stored subreddits", Command.GEN_STORED)],
        [_btn("From post url", Command.GEN_URL)],
    ]

    keyboard = InlineKeyboardMarkup(options)
    await update.message.reply_text("Select generation method:", reply_markup=keyboard)

async def select_subreddit(update: Update, _):
    from core.listings import get_subreddits
    
    options = [
        [_btn(item.name, _p(Command.GEN_STORED, item.name))]
        for item in get_subreddits()
    ]
    keyboard = InlineKeyboardMarkup(options)
    await update.message.reply_text("Select subreddit:", reply_markup=keyboard)

