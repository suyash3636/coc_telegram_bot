import asyncio
import requests
from telegram import Update
from telegram.ext import ContextTypes
from database import get_linked_clans, get_linked_players
from config import COC_API_KEY

# Clash of Clans API headers
HEADERS = {"Authorization": f"Bearer {COC_API_KEY}", "Accept": "application/json"}

# Function to fetch clan details from the API
def get_clan_details_from_api(clan_tag):
    encoded_tag = clan_tag.replace("#", "%23")
    url = f"https://api.clashofclans.com/v1/clans/{encoded_tag}"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            clan_data = response.json()
            return clan_data.get("name", "Unknown"), clan_data.get("clanLevel", "N/A")
        else:
            return "Unknown", "N/A"
    except requests.RequestException:
        return "Unknown", "N/A"

# Telegram command to show user profile
async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id

    # Fetch linked clans
    linked_clans = await asyncio.to_thread(get_linked_clans, telegram_id)
    clan_details = []

    for clan_tag in linked_clans:
        clan_name, clan_level = await asyncio.to_thread(get_clan_details_from_api, clan_tag)
        clan_details.append((clan_tag, clan_name, clan_level))

    # Fetch linked players
    linked_players = await asyncio.to_thread(get_linked_players, telegram_id)

    # Start building the profile message
    profile_msg = f"╔════════════════════════╗\n║  👤 User ID: {telegram_id}\n║\n"

    # Add linked clans
    profile_msg += "║ 🏰 Linked Clans:\n║\n"
    if clan_details:
        for idx, (clan_tag, clan_name, clan_level) in enumerate(clan_details, start=1):
            profile_msg += f"║ {idx}. {clan_name} (Lvl {clan_level})\n║    ➝ {clan_tag}\n"
    else:
        profile_msg += "║ No linked clans found.\n"

    # Add linked players
    profile_msg += "║\n║ 👥 Linked Players:\n║\n"
    if linked_players:
        for idx, (player_name, player_tag) in enumerate(linked_players, start=1):
            profile_msg += f"║ {idx}. {player_name}\n║    ➝ {player_tag}\n"
    else:
        profile_msg += "║ No linked players found.\n"

    profile_msg += "╚════════════════════════╝"

    # Ensure message doesn't exceed Telegram's 4096-character limit
    if len(profile_msg) > 4000:
        msg_parts = [profile_msg[i:i+4000] for i in range(0, len(profile_msg), 4000)]
        for part in msg_parts:
            await update.message.reply_text(f"```\n{part}\n```", parse_mode="MarkdownV2")
    else:
        await update.message.reply_text(f"```\n{profile_msg}\n```", parse_mode="MarkdownV2")
