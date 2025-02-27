import logging
import requests
from telegram import Update
from telegram.ext import CallbackContext
from database import get_linked_clans  # Fetch linked clan from database
from config import COC_API_KEY

# Logger setup
logger = logging.getLogger(__name__)

# Clash of Clans API headers
HEADERS = {"Authorization": f"Bearer {COC_API_KEY}", "Accept": "application/json"}

# Function to fetch current war details
def get_current_war(clan_tag):
    """Fetch ongoing war details from the Clash of Clans API."""
    encoded_tag = clan_tag.replace("#", "%23")
    url = f"https://api.clashofclans.com/v1/clans/{encoded_tag}/currentwar"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()  # Raise an error for HTTP status codes >= 400
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch war details: {e}")
        return None

# Function to fetch clan name
def get_clan_name(clan_tag):
    """Fetch clan details to retrieve the clan name."""
    encoded_tag = clan_tag.replace("#", "%23")
    url = f"https://api.clashofclans.com/v1/clans/{encoded_tag}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        clan_data = response.json()
        return clan_data.get("name", "Unknown Clan")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch clan name: {e}")
        return "Unknown Clan"

# Telegram command to check remaining war attacks
async def warrem(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    # Fetch linked clan tag(s)
    linked_clans = get_linked_clans(user_id)
    if not linked_clans:
        await update.message.reply_text("❌ You have not linked any clans. Use /linkclan to link one.")
        return

    # Determine which clan to use (default: first one)
    clan_index = 0
    if context.args:
        try:
            clan_index = int(context.args[0]) - 1
            if clan_index < 0 or clan_index >= len(linked_clans):
                raise ValueError
        except ValueError:
            await update.message.reply_text(f"❌ Invalid clan selection. Choose from 1 to {len(linked_clans)}.")
            return

    clan_tag = linked_clans[clan_index]
    clan_name = get_clan_name(clan_tag)

    # Fetch war details
    war_data = get_current_war(clan_tag)
    if not war_data or "state" not in war_data:
        await update.message.reply_text(f"❌ Failed to fetch war details for {clan_name}. Try again later.")
        return

    # Check if a war is ongoing
    if war_data["state"] != "inWar":
        await update.message.reply_text(f"⚠️ No ongoing war for {clan_name}.")
        return

    # Get list of players and their attacks
    players = war_data.get("clan", {}).get("members", [])
    remaining_attacks = []

    for player in players:
        name = player.get("name", "Unknown")
        attacks_used = len(player.get("attacks", []))  # Count attacks made
        attacks_left = 2 - attacks_used  # Remaining attacks

        if attacks_left > 0:
            remaining_attacks.append(f"- *{name}* → `{attacks_left}` left")

    # Formatting response
    if not remaining_attacks:
        message = f"✅ All players have completed their attacks in {clan_name}!"
    else:
        message = f"🚨 *{clan_name} - Players with Remaining War Attacks:* 🚨\n\n"
        message += "\n".join(remaining_attacks)

    await update.message.reply_text(message, parse_mode="Markdown")
