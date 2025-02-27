import requests
import mysql.connector
from telegram import Update
from telegram.ext import CallbackContext
from config import COC_API_KEY, MYSQL_CONFIG


def get_clan_info(clan_tag: str):
    """Fetch clan information from Clash of Clans API using requests"""
    url = f"https://api.clashofclans.com/v1/clans/{clan_tag.replace('#', '%23')}"
    headers = {"Authorization": f"Bearer {COC_API_KEY}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to fetch clan info. HTTP {response.status_code}"}


def get_linked_clan(user_id: int, clan_index: int = 1):
    """Retrieve the linked clan tag from MySQL"""
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor(dictionary=True)

        # Fetch the linked clan from the 'clans' table
        cursor.execute(
            "SELECT clan_tag FROM clans WHERE telegram_id = %s ORDER BY id LIMIT %s,1",
            (user_id, clan_index - 1),
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        return result["clan_tag"] if result else None
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return None


async def clan_command(update: Update, context: CallbackContext):
    """Handle /clan command to fetch clan details"""
    user_id = update.message.from_user.id
    clan_index = int(context.args[0]) if context.args else 1  # Default to first clan

    clan_tag = get_linked_clan(user_id, clan_index)
    if not clan_tag:
        await update.message.reply_text("⚠️ You have no linked clans. Use /linkclan to add one.")
        return

    clan_data = get_clan_info(clan_tag)
    if "error" in clan_data:
        await update.message.reply_text(clan_data["error"])
        return

    # Format the response
    clan_info = (
        f"🏰 <b>Clan Name:</b> {clan_data['name']}\n"
        f"🏷️ <b>Clan Tag:</b> {clan_data['tag']}\n"
        f"📈 <b>Clan Level:</b> {clan_data['clanLevel']}\n"
        f"👥 <b>Members:</b> {clan_data['members']}/50\n"
        f"🏆 <b>War Wins:</b> {clan_data.get('warWins', 'N/A')}\n"
        f"🔥 <b>War Win Streak:</b> {clan_data.get('warWinStreak', 'N/A')}\n"
        f"🗓️ <b>War Frequency:</b> {clan_data.get('warFrequency', 'N/A')}\n"
        f"💯 <b>Clan Points:</b> {clan_data.get('clanPoints', 'N/A')}\n"
        f"💪 <b>Clan Versus Points:</b> {clan_data.get('clanVersusPoints', 'N/A')}\n"
        f"🏅 <b>Required Trophies:</b> {clan_data.get('requiredTrophies', 'N/A')}\n"
        f"📍 <b>Location:</b> {clan_data.get('location', {}).get('name', 'Unknown')}\n"
        f"🔗 <b>View Clan:</b> <a href='https://link.clashofclans.com/en?action=OpenClanProfile&tag={clan_data['tag'].replace('#', '%23')}'>Click Here</a>"
    )

    await update.message.reply_text(clan_info, parse_mode="HTML")
