import time
import requests
from telegram import Update
from telegram.ext import ContextTypes
from config import COC_API_KEY

# Clash of Clans API headers
HEADERS = {"Authorization": f"Bearer {COC_API_KEY}", "Accept": "application/json"}

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Checks the response time (ping) for Telegram API and Clash of Clans API."""
    
    # Measure Telegram API latency
    start_telegram = time.time()
    await update.message.reply_text("⏳ Checking ping...")
    telegram_ping = round((time.time() - start_telegram) * 1000, 2)

    # Measure Clash of Clans API latency
    start_coc = time.time()
    url = "https://api.clashofclans.com/v1/clans/%232P0QUR8Q0"  # Example valid clan tag
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            coc_ping = round((time.time() - start_coc) * 1000, 2)
        else:
            coc_ping = "❌ Error"
    except requests.RequestException:
        coc_ping = "❌ Error"

    # Send results
    ping_msg = f"🏓 *Ping Results:*\n\n"
    ping_msg += f"📡 Telegram API: `{telegram_ping}ms`\n"
    ping_msg += f"🔥 Clash of Clans API: `{coc_ping}ms`"
    
    await update.message.reply_text(ping_msg, parse_mode="Markdown")
