-- Use the database
USE Rexx_dbm;

-- Insert Main Admin
INSERT INTO admins (telegram_id, username, role) 
-- Search for @userinfobot on Telegram, start it, and get your User ID instantly.
VALUES (Telegram_userid, 'User_name', 'main_admin')
ON DUPLICATE KEY UPDATE username = 'User_name', role = 'main_admin';

-- Insert Default Settings
INSERT INTO settings (setting_name, value) 
VALUES ('allow_user_linking', 'true')
ON DUPLICATE KEY UPDATE value = 'true';
