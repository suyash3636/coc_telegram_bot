from telegram import Update
from telegram.ext import CallbackContext
import requests
async def start(update: Update, context: CallbackContext):
    message = (
        "Hello! I am your Clash of Clans Bot Rexx. \n\n"
        "Use /help to see available commands."
    )
    await update.message.reply_text(message)
