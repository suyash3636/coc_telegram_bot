# 
# 🏆 Clash of Clans Telegram Bot - Rexx  

A powerful **Telegram bot** built with Python that integrates with the **Clash of Clans API** to provide real-time clan stats, war updates, and more! 🚀  

## 📌 Features  
✅ Link multiple Clash of Clans accounts and clans  
✅ Fetch **clan details, members, war status, and remaining war attacks**  
✅ Check linked **player profiles** and clan statistics  
✅ Admin settings for managing linking permissions  
✅ **Ping command** to check API response times  

---

## 🛠️ Setup & Installation  

### **1️⃣ Clone the Repository**  
 
git clone https://github.com/suyash3636/coc_telegram_bot.git
cd coc_telegram_bot


## 2️⃣ Create a Virtual Environment
 
python3 -m venv venv
source venv/bin/activate  # On Linux/macOS </br>
venv\Scripts\activate      # On Windows

## 3️⃣ Install Dependencies

pip install -r requirements.txt

## 4️⃣ Configure API Keys
Rename .env.example to .env and add your API keys:
 
TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
COC_API_KEY="your_clash_of_clans_api_key"
MYSQL_HOST="localhost"
MYSQL_USER="root"
MYSQL_PASSWORD="yourpassword"
MYSQL_DATABASE="Rexx_dbm"


## 📜 Commands
Command	Description
/start	Start the bot
/help	Show available commands
/linkplayer	Link a player to your account
/linkclan	Link a clan to your account
/clan	Get linked clan details
/members	Get clan members list
/war	Show current war details
/warrem	Show remaining war attacks
/player	Fetch player details
/profile	Show linked players and clans
/adminsettings	Manage bot admin settings

## 📬 Contact
For queries, reach out to suyash3636@gmail.com 