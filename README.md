# littleBox

A Telegram bot that connects people who need to send a small parcel to another city or country with travelers who are already going there.

A sender posts what they want to send and where. A traveler posts their trip. The bot matches the two by route and date, notifies both sides, and gives them a way to get in touch. The deal itself happens between people: littleBox is only the place where they find each other.

The bot ran on Render in spring 2025 with real users and a few successful deliveries. The hosted instance is offline now. The bot talks to users in Russian.

## Features

**For senders**
- Post a parcel: description, origin, destination, date it is relevant until, and price.
- Search for travelers on a route. Exact city matches come first; if there are none, the bot shows travelers from the same country.

**For travelers**
- Post a trip: origin, destination, travel date, free luggage space, and conditions.
- Search for parcels on an exact city-to-city route.

**For everyone**
- Instant notifications: a new parcel reaches travelers on the same route, and a new trip reaches senders waiting on it.
- City names are normalized through OpenStreetMap, so "Bishkek, Kyrgyzstan" and "Бишкек" end up as the same place.
- Contact through Telegram username. If an author has no username, a "Contact the author" button sends them the username of whoever pressed it, so the author can write first.
- "My listings" to edit or delete your own parcels and trips.
- Anti-fraud warning on every new parcel and a `/rules` page with safety tips.
- Feedback form, plus an admin panel with usage stats and the latest feedback.

## How it works

```mermaid
sequenceDiagram
    actor Sender
    participant Bot as littleBox
    participant OSM as Nominatim (OpenStreetMap)
    actor Traveler

    Traveler->>Bot: Post a trip: Bishkek to Belgrade, 12.06
    Sender->>Bot: Post a parcel on the same route
    Bot->>OSM: Normalize city and country
    OSM-->>Bot: Бишкек, Кыргызстан
    Bot-->>Sender: Parcel published
    Bot->>Traveler: New parcel on your route
    Traveler->>Bot: Contact the author (sender has no username)
    Bot->>Sender: @traveler wants to reach you
```

- **Forms.** Each listing is collected step by step with an aiogram finite state machine. Menu buttons work at any step and start their own flow, and non-text messages get a hint instead of breaking the form.
- **Matching.** Parcels and trips match on city and country of both ends. Expired parcels and past trips never appear in search results or notifications.
- **Geocoding.** Nominatim calls run in a worker thread, so a slow lookup never blocks other users. A timeout or outage gets a "try again" reply.
- **Safety.** User input is HTML-escaped before it goes into messages. A per-user rate limit protects against flooding.

## Commands

| Command | What it does |
| --- | --- |
| `/start` | Register and show the main menu |
| `/help` | List what the bot can do |
| `/cancel` | Drop the current form and return to the menu |
| `/rules` | Safety rules |
| `/admin` | Admin panel (admin only) |
| `/stats` | Number of users, parcels, trips and feedback messages (admin only) |
| `/feedbacks` | The five latest feedback messages (admin only) |

Most actions are available from the main menu keyboard: send a parcel, post a trip, find a traveler, find a parcel, my listings, feedback, and safety.

## Tech stack

- Python 3.10+
- [aiogram 3](https://docs.aiogram.dev/): routers, FSM, filters, middlewares
- SQLAlchemy 2 (async) with PostgreSQL through asyncpg
- geopy with Nominatim for geocoding
- pytest with pytest-asyncio, SQLite through aiosqlite for tests

## Getting started

You need Python 3.10+ on Linux or macOS, a PostgreSQL database, and a bot token from [@BotFather](https://t.me/BotFather).

```bash
git clone https://github.com/ShabdanDzhumabekov/littleBox-bot.git
cd littleBox-bot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```dotenv
BOT_TOKEN=123456:your-bot-token
ADMIN_ID=123456789
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/littlebox
```

| Variable | Meaning |
| --- | --- |
| `BOT_TOKEN` | Token from @BotFather |
| `ADMIN_ID` | Telegram user id that gets the admin panel |
| `DATABASE_URL` | SQLAlchemy async URL of the PostgreSQL database |

Create the tables once, then start the bot:

```bash
python -m bot.database.create_db
python -m bot.main
```

The bot uses long polling, so it needs no public URL or webhook.

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```

The suite needs no bot token, network or PostgreSQL, and runs in about two seconds:

- The Telegram Bot API is replaced by a fake session that records every outgoing message and button answer.
- The database is a local SQLite file through aiosqlite.
- Nominatim is replaced by a fake geocoder with a fixed set of places.

Tests go through the same dispatcher and routers as production updates, so they check what a user would actually see. They live next to the code they cover, as `test_*.py`.

## Project structure

```
bot/
├── main.py          entry point: bot, dispatcher, middlewares, polling
├── config.py        settings from environment variables or .env
├── constants.py     text length limits and the anti-fraud warning
├── database/        SQLAlchemy models, engine, table creation script
├── handlers/        one router per feature: listings, search, contact, admin, ...
├── keyboards/       reply and inline keyboards
├── filters/         IsAdmin, IsFreeText
├── middlewares/     per-user rate limiting
├── states/          FSM states for the forms
├── utils/           geocoding, formatting, notifications, validation
└── testing/         fakes and builders shared by the tests
```

## Deployment

On Render the bot ran as a background worker (see `Procfile`) with a managed PostgreSQL database. Form progress lives in memory, so run a single instance and expect unfinished forms to reset after a restart.

## Roadmap

- Docker image and CI that runs the tests on every push
- Alembic migrations instead of `create_db`
- Typed settings that fail fast on a missing variable
- Respect Nominatim's one-request-per-second policy and cache lookups
- Keep stored usernames in sync after registration
- English interface

See [CHANGELOG.md](CHANGELOG.md) for release history.

## Author

Built by Shabdan Dzhumabekov. Questions and ideas are welcome on Telegram at [@Justshaba](https://t.me/Justshaba).
