import pymysql
import requests
from config import COC_API_KEY, MYSQL_CONFIG, TELEGRAM_BOT_TOKEN  # ✅ Import from config

COC_API_URL = "https://api.clashofclans.com/v1/players/"

# 🔹 Database Connection
def get_db_connection():
    """Establish and return a database connection."""
    return pymysql.connect(**MYSQL_CONFIG)

# 🔹 Check if user linking is enabled
def is_linking_allowed():
    """Check if user linking is allowed based on settings."""
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT value FROM settings WHERE setting_name = 'allow_user_linking'")
    result = cursor.fetchone()
    db.close()
    return result and result[0] == "true"

# 🔹 Check if user is an admin
def is_admin(telegram_id):
    """Check if a given Telegram user is an admin."""
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT role FROM admins WHERE telegram_id = %s", (telegram_id,))
    result = cursor.fetchone()
    db.close()
    return result is not None  # ✅ Returns True if user is an admin

# 🔹 Fetch player details from Clash of Clans API
def get_player_info(player_tag):
    """Fetch player details from the Clash of Clans API."""
    headers = {"Authorization": f"Bearer {COC_API_KEY}"}
    url = COC_API_URL + player_tag.replace("#", "%23")  # Convert '#' to '%23'

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    return None

# 🔹 Link a player to a Telegram user
def link_player(telegram_id, player_tag):
    """Links a player to a Telegram account if allowed by settings."""
    if not is_linking_allowed() and not is_admin(telegram_id):
        return "🚫 User linking is currently disabled by admins."

    player_data = get_player_info(player_tag)
    if not player_data:
        return "❌ Invalid player tag or unable to fetch player details."

    player_name = player_data.get("name", "Unknown")

    db = get_db_connection()
    cursor = db.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO players (telegram_id, player_tag, player_name) VALUES (%s, %s, %s)",
            (telegram_id, player_tag, player_name)  
        )
        db.commit()
        return f"✅ Successfully linked {player_name} ({player_tag}) to your account."
    except pymysql.IntegrityError:
        return "⚠️ This player is already linked."
    finally:
        db.close()

# 🔹 Link a clan to a Telegram user
def link_clan(telegram_id, clan_tag):
    """Links a clan to a Telegram user if allowed by settings."""
    if not is_linking_allowed() and not is_admin(telegram_id):
        return "🚫 Clan linking is currently disabled by admins."

    db = get_db_connection()
    cursor = db.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO clans (telegram_id, clan_tag, clan_name) VALUES (%s, %s, %s)",
            (telegram_id, clan_tag, "Unknown Clan")
        )
        db.commit()
        return f"✅ Clan {clan_tag} has been linked successfully."
    except pymysql.IntegrityError:
        return "⚠️ This clan is already linked."
    finally:
        db.close()

# 🔹 Fetch the linked clan for a user
def get_linked_clans(telegram_id):
    """Fetch all linked clan tags for a user"""
    db = get_db_connection()
    cursor = db.cursor()
    
    cursor.execute("SELECT clan_tag FROM clans WHERE telegram_id = %s", (telegram_id,))
    result = cursor.fetchall()

    cursor.close()
    db.close()

    return [row[0] for row in result]  # Return a list of clan tags (strings)

# 🔹 Fetch clan details
def get_clan_details(clan_tag):
    """Fetch clan name and level from the database using clan_tag"""
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("SELECT clan_name FROM clans WHERE clan_tag = %s", (clan_tag,))
    result = cursor.fetchone()

    cursor.close()
    db.close()

    if result:
        clan_name = result[0]
    else:
        clan_name = "Unknown Clan"

    return clan_name  # Only return clan_name

# 🔹 Debugging function to test connection
def test_db_connection():
    """Test database connection and print result."""
    try:
        db = get_db_connection()
        print("✅ Database connection successful!")
        db.close()
    except Exception as e:
        print(f"❌ Database connection failed: {e}")

# 🔹 Print the Telegram bot token for debugging (optional)
def test_bot_token():
    """Prints the Telegram bot token to verify it is loaded correctly."""
    print(f"🤖 Telegram Bot Token: {TELEGRAM_BOT_TOKEN}")
def get_user_linking_status():
    """Fetch the latest user linking status from the database."""
    db = pymysql.connect(**MYSQL_CONFIG)
    cursor = db.cursor()
    cursor.execute("SELECT value FROM settings WHERE setting_name = 'allow_user_linking'")
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return result[0] == "true" if result else False
def get_linked_players(telegram_id):
    """Fetch linked players of a user."""
    query = "SELECT player_name, player_tag FROM players WHERE telegram_id = %s"
    db = pymysql.connect(**MYSQL_CONFIG)
    cursor = db.cursor()
    cursor.execute(query, (telegram_id,))
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return results  # List of (player_name, player_tag)

# ✅ Run tests
if __name__ == "__main__":
    test_db_connection()
    test_bot_token()
