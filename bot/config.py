"""
Загрузка конфигурации из .env файла для безопасного хранения данных.
"""

from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Данные PostgreSQL
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

if __name__ == "__main__":
    print("BOT_TOKEN:", BOT_TOKEN)
    print("DB_NAME:", DB_NAME)
    print("DB_USER:", DB_USER)
    print("DB_PASSWORD:", DB_PASSWORD)
    print("DB_HOST:", DB_HOST)
    print("DB_PORT:", DB_PORT)