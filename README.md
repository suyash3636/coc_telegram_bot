# 
# 🏆 Clash of Clans Telegram Bot - Rexx  

A powerful **Telegram bot** built with Python that integrates with the **Clash of Clans API** to provide real-time clan stats, war updates, and more! 🚀  

## 📌 Features  
✅ Link multiple Clash of Clans accounts and clans  
✅ Fetch **clan details, members, war status, and remaining war attacks**  
✅ Check linked **player profiles** and clan statistics  
✅ Admin settings for managing linking permissions  
✅ **Ping command** to check API response times.

---

## 🛠️ Setup & Installation  

### **1️⃣ Clone the Repository**  
 
git clone https://github.com/suyash3636/coc_telegram_bot.git</br>
cd coc_telegram_bot


## 2️⃣ Create a Virtual Environment
 
python3 -m venv venv
source venv/bin/activate  # On Linux/macOS </br>
venv\Scripts\activate      # On Windows

## 3️⃣ Install Dependencies

pip install -r requirements.txt</br>

## 4️⃣ Configure API Keys
Rename .env.example to .env and add your API keys:</br>
 
TELEGRAM_BOT_TOKEN="your_telegram_bot_token"</br>
COC_API_KEY="your_clash_of_clans_api_key"</br>
MYSQL_HOST="localhost"</br>
MYSQL_USER="root"</br>
MYSQL_PASSWORD="yourpassword"</br>
MYSQL_DATABASE="Rexx_dbm"</br>


## 📜 Commands
Command	Description</br>
/start	Start the bot</br>
/help	Show available commands</br>
/linkplayer	Link a player to your account</br>
/linkclan	Link a clan to your account</br>
/clan	Get linked clan details</br>
/members	Get clan members list</br>
/war	Show current war details</br>
/warrem	Show remaining war attacks</br>
/player	Fetch player details</br>
/profile	Show linked players and clans</br>
/adminsettings	Manage bot admin settings</br>

## 📬 Contact

For queries, reach out to suyash3636@gmail.com </br>