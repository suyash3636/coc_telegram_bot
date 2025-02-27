import requests
import mysql.connector
from telegram import Update
from telegram.ext import CallbackContext
from config import COC_API_KEY, MYSQL_CONFIG

# Function to get player data from Clash of Clans API
def get_player_info(player_tag):
    url = f"https://api.clashofclans.com/v1/players/{player_tag.replace('#', '%23')}"
    headers = {"Authorization": f"Bearer {COC_API_KEY}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

# Function to get linked player tag from the database
def get_linked_player(telegram_id, index=1):
    try:
        conn = mysql.connector.connect(**MYSQL_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute(
            "SELECT player_tag FROM players WHERE telegram_id = %s ORDER BY id LIMIT %s,1",
            (telegram_id, index - 1)  # Adjust index to start from 0
        )
        result = cursor.fetchone()
        
        conn.close()
        return result["player_tag"] if result else None
    except Exception as e:
        print(f"Database error: {e}")
        return None

# Command handler for /player
async def player_command(update: Update, context: CallbackContext):
    telegram_id = update.message.from_user.id
    
    # Check if user provided a specific player tag
    if context.args:
        player_tag = context.args[0]
    else:
        # Fetch the first linked player if no tag is given
        player_tag = get_linked_player(telegram_id)

    if not player_tag:
        await update.message.reply_text("You have no linked players. Use /linkplayer to link a player.")
        return

    # Fetch player data from API
    player_data = get_player_info(player_tag)
    if not player_data:
        await update.message.reply_text("Failed to fetch player data. Please check the tag and try again.")
        return

    # Extract relevant data
    name = player_data.get("name", "N/A")
    tag = player_data.get("tag", "N/A")
    exp = player_data.get("expLevel", "N/A")
    clan = player_data.get("clan", {}).get("name", "No Clan")
    clan_tag = player_data.get("clan", {}).get("tag", "N/A")
    role = player_data.get("role", "Member").replace("admin", "CoLeader").replace("leader", "Leader")
    th_level = player_data.get("townHallLevel", "N/A")
    bh_level = player_data.get("builderHallLevel", "N/A")
    hv_trophies = player_data.get("trophies", "N/A")
    bb_trophies = player_data.get("builderBaseTrophies", "N/A")
    league = player_data.get("league", {}).get("name", "Unranked")
    attack_wins = player_data.get("attackWins", "0")
    defense_wins = player_data.get("defenseWins", "0")
    donations = player_data.get("donations", "0")
    donations_received = player_data.get("donationsReceived", "0")
    war_stars = player_data.get("warStars", "0")
    cwl_stars = player_data.get("clanWarLeagueStars", "0")  # Fixed CWL stars
    clan_games = next((a["value"] for a in player_data.get("achievements", []) if a["name"] == "Games Champion"), "N/A")

    # Extract heroes and pets
    heroes = {h["name"]: h["level"] for h in player_data.get("heroes", [])}

    # Hero names mapping (including Minion Prince)
    hero_names = {
        "Barbarian King": "BK", "Archer Queen": "AQ", "Grand Warden": "GW", "Royal Champion": "RC",
        "Minion Prince": "MP"  , "Battle Machine": "BM", "Battle Copter": "BC"# Minion Prince added
    }
    formatted_heroes = " ".join([f"{hero_names.get(h, h)} ({heroes[h]})" for h in hero_names if h in heroes])

    # Format output message with emojis
    player_info = (
        f"👑 **{name}** ({tag})\n\n"
        f"🎖️ **Exp:** {exp}\n"
        f"🏰 **Clan:** {clan} ({clan_tag})\n"
        f"🎭 **Role:** {role}\n"
        f"🏠 **TH/BH:** {th_level}/{bh_level}\n"
        f"🏆 **HV/BB Trophies:** {hv_trophies}/{bb_trophies}\n"
        f"⚔️ **League:** {league}\n"
        f"⚔️ **Atk/Def:** {attack_wins}/{defense_wins}\n"
        f"🎁 **Don/Rec:** {donations}/{donations_received}\n"
        f"🌟 **War/CWL Stars:** {war_stars}/{cwl_stars}\n"
        f"🎮 **Clan Games:** {clan_games}\n\n"
        f"🦸 **Heroes:** {formatted_heroes}"
    )

    await update.message.reply_text(player_info, parse_mode="Markdown")
