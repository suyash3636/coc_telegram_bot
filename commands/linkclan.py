import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from database import link_clan, is_admin, get_user_linking_status

async def link_clan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id

    if not context.args:
        await update.message.reply_text("Usage: /linkclan #clan_tag")
        return

    clan_id = context.args[0]
    is_admin_user = await asyncio.to_thread(is_admin, telegram_id)
    linking_enabled = await asyncio.to_thread(get_user_linking_status)

    if not linking_enabled and not is_admin_user:
        await update.message.reply_text("🚫 Linking is currently disabled by the admin.")
        return

    response = await asyncio.to_thread(link_clan, telegram_id, clan_id)
    await update.message.reply_text(response)
