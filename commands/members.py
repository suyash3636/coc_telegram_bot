import logging
import html
import requests
from telegram import Update
from telegram.ext import CallbackContext
from database import get_linked_clans  # Fetch linked clan tags from database
from config import COC_API_KEY  # Import API Key

# Logger Setup
logger = logging.getLogger(__name__)

# Role Mapping for Readability
role_mapping = {
    "leader": "👑 Leader",
    "coLeader": "⚔️ Co-Leader",
    "admin": "🛡️ Elder",
    "member": "👥 Member"
}

# Function to escape HTML characters
def escape_html(text):
    return html.escape(text)

# Fetch and Send Clan Members List
async def members(update: Update, context: CallbackContext) -> None:
    logger.info("🔹 Fetching clan members...")

    telegram_id = update.message.from_user.id

    # Fetch linked clans from database (returns a list)
    linked_clans = get_linked_clans(telegram_id)
    if not linked_clans:
        await update.message.reply_text("❌ You have not linked any clans. Use /linkclan <clan_id> to link one.")
        return

    # Determine which clan to use
    clan_index = 0  # Default to the first linked clan
    if context.args:
        try:
            clan_index = int(context.args[0]) - 1
            if clan_index < 0 or clan_index >= len(linked_clans):
                raise ValueError
        except ValueError:
            await update.message.reply_text(f"❌ Invalid clan selection. Choose from 1 to {len(linked_clans)}.")
            return

    clan_tag = linked_clans[clan_index]  # Select the clan tag
    if not isinstance(clan_tag, str):
        await update.message.reply_text("❌ Error retrieving clan tag. Please try again.")
        return

    # Fetch clan details (to get the clan name)
    encoded_tag = clan_tag.replace("#", "%23")
    clan_url = f"https://api.clashofclans.com/v1/clans/{encoded_tag}"
    members_url = f"https://api.clashofclans.com/v1/clans/{encoded_tag}/members"
    headers = {"Authorization": f"Bearer {COC_API_KEY}"}

    try:
        # Fetch clan details
        clan_response = requests.get(clan_url, headers=headers)
        if clan_response.status_code != 200:
            await update.message.reply_text("❌ Failed to fetch clan details. Please check the clan tag and try again.")
            return

        clan_data = clan_response.json()
        clan_name = escape_html(clan_data.get("name", "Unknown"))

        # Fetch clan members
        members_response = requests.get(members_url, headers=headers)
        if members_response.status_code != 200:
            await update.message.reply_text("❌ Failed to fetch clan members.")
            return

        members_data = members_response.json()
        members_list = members_data.get("items", [])

        if not members_list:
            await update.message.reply_text(f"⚠️ No members found in the clan {clan_name}.")
            return

        # Start building the message
        message = f"<b>🔥 Clan Members List: {clan_name} ({clan_tag})</b>\n\n"

        for index, member in enumerate(members_list, start=1):
            name = escape_html(member.get("name", "Unknown"))
            trophies = escape_html(str(member.get("trophies", "N/A")))
            role = escape_html(role_mapping.get(member.get("role", "N/A"), "Unknown"))

            index_emoji = ''.join(f"{int(digit)}️⃣" for digit in str(index))
            message += f"{index_emoji} | <b>{name}</b> | 🏆 {trophies} | {role}\n"

        # Send formatted message using HTML parse mode
        await update.message.reply_text(message, parse_mode="HTML")

    except Exception as e:
        logger.error(f"❌ Error fetching clan members: {e}")
        await update.message.reply_text("⚠️ An error occurred while fetching clan members. Please try again later.")
