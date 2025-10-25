"""
Configuration file for INEX CONSULTING Telegram Bot
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Bot Token
BOT_TOKEN = os.getenv('BOT_TOKEN', '8236382244:AAHCRDBqKpIwo9jHYgr4lA-sTjriMBjwgZs')

# Channel Configuration
# CHANNEL_ID = '@man_ku_bu'
CHANNEL_ID = '@InEx_Operations'
# CHANNEL_URL = 'https://t.me/man_ku_bu'
CHANNEL_URL = 'https://t.me/InEx_Operations'

# Admin IDs (Telegram user IDs)
ADMIN_IDS = [
    int(id_) for id_ in os.getenv('ADMIN_IDS', '').split(',') if id_.strip()
]

# Database
DB_PATH = 'inex_bot.db'

# Languages
LANGUAGES = ['uz', 'ru']
DEFAULT_LANGUAGE = 'uz'

# Validation patterns
PHONE_PATTERN = r'^\+?998[0-9]{9}$'  # Uzbekistan phone format
