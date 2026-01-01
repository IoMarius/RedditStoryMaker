from telegram import Update
from telegram.ext import ContextTypes
from telegram.helpers import escape_markdown
import core.generator as gen
from .utils import Command


async def generate_from_stored_sub(
    update: Update, context: ContextTypes.DEFAULT_TYPE, parameter: any = None
) -> None:
    async def callback(msg: str):
        await update.callback_query.edit_message_text(msg)

    result = await gen.run_generation_pipeline_async(parameter, callback)
    await callback("📹➡️ Sending video...")

    main = escape_markdown(result.caption, version=2)
    italic = escape_markdown(result.hashtags, version=2)

    with open(result.video_path, "rb") as video:
        user_id = update.effective_user.id
        await context.bot.send_video(
            chat_id=user_id,
            video=video,
            caption=f"{main}\n_{italic}_",
            parse_mode="MarkdownV2",
        )

    await callback("✅ Done!")


dispatch_table = {
    Command.GEN_STORED: generate_from_stored_sub,
}
