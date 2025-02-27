from telegram import Update
from telegram.ext import ContextTypes
import asyncio
from database import is_admin, get_db_connection

async def adminsettings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /adminsettings command to toggle allow_user_linking."""
    telegram_id = update.message.from_user.id
    print(f"🔹 AdminSettings command triggered by: {telegram_id}")  # Debugging

    # Check if the user is an admin
    is_admin_user = await asyncio.to_thread(is_admin, telegram_id)
    print(f"🔹 Is Admin: {is_admin_user}")  # Debugging
    if not is_admin_user:
        await update.message.reply_text("🚫 Only admins can change settings.")
        return

    # Connect to database
    db = get_db_connection()
    cursor = db.cursor()

    # Get current setting value
    cursor.execute("SELECT value FROM settings WHERE setting_name = 'allow_user_linking'")
    result = cursor.fetchone()
    print(f"🔹 Current Setting: {result}")  # Debugging

    if result:
        new_value = "false" if result[0] == "true" else "true"
        cursor.execute(
            "UPDATE settings SET value = %s WHERE setting_name = 'allow_user_linking'",
            (new_value,)
        )
    else:
        new_value = "true"  # Default to enabling if setting is missing
        cursor.execute(
            "INSERT INTO settings (setting_name, value) VALUES ('allow_user_linking', %s)",
            (new_value,)
        )

    db.commit()
    db.close()

    # Send confirmation message
    status = "✅ User linking is now ENABLED." if new_value == "true" else "❌ User linking is now DISABLED."
    print(f"🔹 New Setting: {new_value}")  # Debugging
    await update.message.reply_text(status)
