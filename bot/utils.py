from enum import Enum
from telegram import InlineKeyboardButton, Update
from telegram.ext import ContextTypes


class Command(str, Enum):
    GEN_STORED = "1"
    GEN_URL = "2"


# class Menu(str, Enum):
#     GEN_TYPE = "1"
#     SEL_SUB = "2"


def _btn(text: str, cmd: Command | str) -> InlineKeyboardButton:
    if isinstance(cmd, Command):
        cmd = cmd.value

    return InlineKeyboardButton(text, callback_data=cmd)


def _p(cmd: Command, param: str | int) -> str:
    return f"{cmd.value}|{param}"


def _parse_cmd(cmd: str) -> tuple[str, str | None, bool]:
    if "|" in cmd:
        k, p = cmd.split("|", 1)
        return k, p, True

    return cmd, None, False


def _get_p(cmd: str) -> str:
    return


def _reply_cmd(update: Update, message: str):
    return update.callback_query.edit_message_text(message)

def _reply(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
    user_id = update.effective_user.id
    return context.bot.send_message(chat_id=user_id, text=message)

