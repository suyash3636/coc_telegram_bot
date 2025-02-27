import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from database import link_player, is_admin, is_linking_allowed

async def link_player_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id

    if not context.args:
        await update.message.reply_text("Usage: /linkplayer #player_tag")
        return

    player_tag = context.args[0]
    is_admin_user = await asyncio.to_thread(is_admin, telegram_id)
    linking_enabled = await asyncio.to_thread(is_linking_allowed)

    if not linking_enabled and not is_admin_user:
        await update.message.reply_text("🚫 Linking is currently disabled by the admin.")
        return

    response = await asyncio.to_thread(link_player, telegram_id, player_tag)
    await update.message.reply_text(response)
