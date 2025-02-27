from telegram import Update
from telegram.ext import Application, CommandHandler
from config import TELEGRAM_BOT_TOKEN
from commands.members import members
from commands.clan import clan_command
from commands.war import war
from commands.warrem import warrem
from commands.player import player_command
from commands.help import help_command
from commands.linkplayer import link_player_command
from commands.linkclan import link_clan_command
from commands.adminsettings import adminsettings_command
from commands.profile import profile_command  # ✅ Import profile command
from commands.ping import ping  # ✅ Import ping command

async def start(update: Update, context):
    await update.message.reply_text("Welcome to the bot! Type /help to see the available commands.")

async def error_handler(update: Update, context):
    print(f"Error: {context.error}")

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("linkplayer", link_player_command))
    app.add_handler(CommandHandler("linkclan", link_clan_command))
    app.add_handler(CommandHandler("clan", clan_command))
    app.add_handler(CommandHandler("members", members))
    app.add_handler(CommandHandler("war", war))
    app.add_handler(CommandHandler("warrem", warrem))
    app.add_handler(CommandHandler("player", player_command))
    app.add_handler(CommandHandler("adminsettings", adminsettings_command))
    app.add_handler(CommandHandler("profile", profile_command))  # ✅ Add profile command
    app.add_handler(CommandHandler("ping", ping))  # ✅ Add ping command

    app.add_error_handler(error_handler)

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
