from dotenv import load_dotenv
import os

load_dotenv()
DB_FILEPATH = r"data/database.db"
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
AI_TOKEN = os.getenv("AI_TOKEN")
