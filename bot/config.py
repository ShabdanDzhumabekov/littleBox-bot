"""
Загрузка конфигурации из .env файла для безопасного хранения данных.
"""

from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Строка подключения к базе данных
DATABASE_URL = os.getenv("DATABASE_URL")