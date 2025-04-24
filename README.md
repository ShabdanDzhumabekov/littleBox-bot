# 📦 LittleBox — Telegram-бот для обмена посылками и поиска попутчиков

LittleBox — это Telegram-бот, с помощью которого пользователи из разных стран могут:
- 📤 Отправить или 📥 Получить небольшую посылку
- 🛫 Разместить маршрут путешествия
- 🔍 Найти попутчика или подходящую посылку
- 📋 Управлять своими объявлениями
- 💬 Оставлять отзывы

---

## 🚀 Возможности

- Регистрация пользователей через `/start`
- Размещение объявлений и маршрутов
- Поиск по точным направлениям
- Редактирование и удаление записей
- Просмотр всех своих объявлений
- Оставление отзывов
- Админ-панель со статистикой и отзывами

---

## 🧠 Стек технологий

- **Python 3.10+**
- **Aiogram 3** — Telegram-бот фреймворк
- **SQLAlchemy** — ORM для PostgreSQL
- **PostgreSQL** — база данных
- **Geopy + Nominatim (OpenStreetMap)** — геокодинг городов и стран
- **FSMContext** — управление состояниями

---

## 📂 Структура проекта
bot/
├── main.py                # Точка входа
├── handlers/              # Все обработчики сообщений и команд
├── keyboards/             # Клавиатуры (reply / inline)
├── states/                # FSM состояния
├── utils/                 # Утилиты (локация, календарь, форматтеры)
├── database/              # Модели и доступ к БД
├── filters/               # Кастомные фильтры (например, IsAdmin)

---

## ⚙️ Установка и запуск

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/yourname/littlebox.git
cd littlebox

# 2. Создайте и активируйте виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# 3. Установите зависимости
pip install -r requirements.txt

# 4. Создайте файл .env и укажите данные


## Пример .env
BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=postgresql+asyncpg://user:password@localhost/littlebox
ADMIN_ID=123456789


# 5. Запустите бота
python -m bot.main


🤝 Контрибьютинг

Буду рад, если вы предложите улучшения или откроете Pull Request!

⸻

©️ Автор

Created with ❤️ by @Justshaba