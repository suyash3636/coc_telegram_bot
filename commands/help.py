from telegram import Update
from telegram.ext import ContextTypes

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "✅ /start - Start the bot\n"
        "❓ /help - Show available commands\n"
        "🏆 /clan - Get clan information\n"
        "⚔️ /war - Get current war details\n"
        "👥 /members - List clan members\n"
        "⚠️ /warrem - Players who haven’t attacked in war\n"
        "🎮 /linkplayer <game_account_id> - Link your game account\n"
        "🏰 /linkclan <clan_id> - Link your clan\n"
        "👤 /player - Get player information\n"
        "👤 /profile - Get linked clan and player info\n"
        " /ping - Get bot latency\n"
    )  
    await update.message.reply_text(help_text)
