📦 LittleBox Bot

Telegram-бот для размещения и поиска небольших посылок, которые можно передать через путешественников.

🚀 Функционал
	•	🔍 Поиск попутчиков и посылок
	•	📦 Размещение объявлений (отправка/получение)
	•	🛫 Размещение маршрутов путешествий
	•	📋 Управление личными объявлениями и маршрутами
	•	💬 Оставление отзывов
	•	🛠 Админ-панель: статистика и отзывы
	•	🔔 Уведомления о совпадениях маршрутов и посылок
	•	🧠 Умная валидация, антиспам, лимиты, логика по срокам

⚙️ Установка
	1.	Клонировать репозиторий:
        git clone https://github.com/your-name/littlebox-bot.git
        cd littlebox-bot

	2.	Установить зависимости:
        python -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt 

    3.	Создать файл .env:
        BOT_TOKEN=your_bot_token
        ADMIN_ID=your_telegram_id
        DATABASE_URL=postgresql+asyncpg://user:password@localhost/dbname
    
    4.	Инициализировать базу данных:
        python -m bot.database.create_db
    
    5.	Запустить бота:
        python -m bot.main

🧱 Стек технологий
	•	Python 3.10+
	•	Aiogram 3.7+
	•	SQLAlchemy (async) + PostgreSQL
	•	Geopy + Nominatim
	•	FSM (машина состояний)
	•	Middlewares / Filters / Routers

💡 Roadmap
	•	📈 Улучшение аналитики
	•	🧼 Антиспам-фильтр для плохих слов
	•	🧪 Unit/авто тесты
	•	🌍 Расширение на другие языки


🤝 Контрибьютинг

Буду рад, если вы предложите улучшения или откроете Pull Request!

⸻

🧑‍💻 Автор

Шабдан Джумабеков — Software | ML Engineer.
Если будут вопросы или предложения, пишите в Telegram: @Justshaba

Created with ❤️ by @Justshaba