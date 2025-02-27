import requests
import mysql.connector
from datetime import datetime, timezone, timedelta
from config import COC_API_KEY, MYSQL_CONFIG
from telegram import Update
from telegram.ext import CallbackContext

# Clash of Clans API Base URL
COC_API_URL = "https://api.clashofclans.com/v1"

def get_linked_clan(telegram_id):
    """Fetch the linked clan tag for a given Telegram user from the database."""
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT clan_tag FROM clans WHERE telegram_id = %s LIMIT 1", (telegram_id,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()
        
        return result["clan_tag"] if result else None
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return None

def fetch_clan_war(clan_tag):
    """Fetch ongoing war details for the given clan tag from the Clash of Clans API."""
    try:
        headers = {"Authorization": f"Bearer {COC_API_KEY}"}
        clan_tag_encoded = clan_tag.replace("#", "%23")
        url = f"{COC_API_URL}/clans/{clan_tag_encoded}/currentwar"

        response = requests.get(url, headers=headers)
        data = response.json()

        if "reason" in data:
            return {"error": data.get("message", "Unknown error occurred.")}

        return data
    except requests.RequestException as e:
        return {"error": str(e)}

def convert_war_end_time(iso_time):
    """Convert ISO 8601 war end time to readable format without using `pytz`."""
    try:
        # Convert war end time to UTC datetime
        war_end_utc = datetime.strptime(iso_time, "%Y%m%dT%H%M%S.%fZ").replace(tzinfo=timezone.utc)

        # Get current UTC time
        now_utc = datetime.now(timezone.utc)

        # Calculate remaining time
        time_remaining = war_end_utc - now_utc
        days = time_remaining.days
        hours, remainder = divmod(time_remaining.seconds, 3600)
        minutes = remainder // 60

        return f"{days}d {hours}h {minutes}m"
    except Exception:
        return "Unknown"

async def war(update: Update, context: CallbackContext):
    """Handle the /war command and send war details."""
    telegram_id = update.message.from_user.id
    clan_tag = get_linked_clan(telegram_id)

    if not clan_tag:
        await update.message.reply_text("⚠️ You have no linked clans. Use /linkclan to add one.")
        return

    war_data = fetch_clan_war(clan_tag)

    if "error" in war_data:
        await update.message.reply_text(f"❌ Error: {war_data['error']}")
        return

    # Fetch details
    clan_name = war_data.get("clan", {}).get("name", "Unknown Clan")
    opponent_name = war_data.get("opponent", {}).get("name", "Unknown Opponent")
    state = war_data.get("state", "Unknown").lower()
    stars = war_data.get("clan", {}).get("stars", 0)
    opp_stars = war_data.get("opponent", {}).get("stars", 0)
    destruction = war_data.get("clan", {}).get("destructionPercentage", 0.0)
    opp_destruction = war_data.get("opponent", {}).get("destructionPercentage", 0.0)
    team_size = war_data.get("teamSize", 0)
    attacks_used = war_data.get("clan", {}).get("attacks", 0)
    max_attacks = team_size * 2
    war_end_time = convert_war_end_time(war_data.get("endTime", "Unknown"))

    # Format response
    war_message = (
        f"🏰 <b>War Details ({clan_name})</b> 🏰\n\n"
        f"⚔️ <b>State:</b> {state}\n"
        f"🛡️ <b>Clan:</b> {clan_name}\n"
        f"🆚 <b>Opponent:</b> {opponent_name}\n"
        f"⭐️ <b>Stars:</b> {stars} - {opp_stars}\n"
        f"🔥 <b>Destruction:</b> {destruction:.1f}% - {opp_destruction:.1f}%\n"
        f"👥 <b>Team Size:</b> {team_size}\n"
        f"⚔️ <b>Attacks Used:</b> {attacks_used} / {max_attacks}\n"
        f"🏆 <b>War Type:</b> {war_data.get('warType', 'Unknown')}\n"
        f"🕒 <b>War Ends In:</b> {war_end_time}\n"
        f"🏅 <b>Result:</b> {state.capitalize()}"
    )

    await update.message.reply_text(war_message, parse_mode="HTML")
