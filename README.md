# Same sticker TG-bot

[![License](https://img.shields.io/badge/license-MIT-blue.svg)]() 
[![Docker](https://img.shields.io/badge/package-Docker_compose-blue.svg)]()

Telegram bot which sends stickers with same emoji as it received.
User sends a sticker, bot sends another sticker with the same ✨️️️️️️️️vibe✨️️️️️️️.

--- 

## 🚀 Features

- Gets messages from users 
- When message contains a sticker, sends a sticker in response
- When there is no response, sends a sorry text

--- 

## 📦 Installation

Clone repository:

```bash 
git clone https://github.com/loginchik/Same-Sticker-Bot.git
```

Move to project directory:

```bash 
cd Same-Sticker-Bot
```


Run docker compose container:

```bash
docker compose up --build --detach 
```