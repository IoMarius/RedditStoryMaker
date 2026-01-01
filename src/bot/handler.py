from telegram import Update
from .utils import _parse_cmd, _reply_cmd
from .dispatch_table import dispatch_table
from telegram.ext import ContextTypes
from core import logger


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    ran = await _handle_cmd(update, context, query.data)

    if not ran:
        await query.edit_message_text(text="Invalid command.")


async def _handle_cmd(
    update: Update, context: ContextTypes.DEFAULT_TYPE, cmd: str | None
) -> bool:
    if cmd is None:
        logger.warning("Command is NONE.")
        return False

    key, param, _ = _parse_cmd(cmd)

    func = dispatch_table.get(key)
    if not func:
        logger.warning(f"Command '{cmd}' not found ind dispatch_table.")
        return False

    # await _reply_cmd(update, "Ok")
    await func(update, context, param)

    return True
