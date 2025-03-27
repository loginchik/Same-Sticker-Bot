import aiofiles
import asyncio
from collections import defaultdict
from itertools import chain
import json
import logging
import os.path
from pathlib import Path
from random import choice

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters.command import CommandStart, Command

from .settings import settings


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M')
logger = logging.getLogger(__name__)

BOT = Bot(token=settings.BOT_TOKEN)
dispatcher = Dispatcher()


async def load_json_data(filepath: str | Path, target_dict: dict) -> None:
    """
    Loads data from JSON file and updates the target dict

    Args:
        filepath (str | Path): Path to JSON file
        target_dict (dict): Dictionary to update
    """
    # Load data from existent file
    if os.path.exists(filepath):
        async with aiofiles.open(filepath, mode='r') as f:
            data = await f.read()
            data = json.loads(data)
        # Update empty dict with values
        target_dict.update(data)


stickers_lock = asyncio.Lock()
users_lock = asyncio.Lock()

async def save_json_data(filepath: str | Path, target_dict: dict, lock: asyncio.Lock) -> None:
    """
    Saves data from dictionary to JSON file

    Args:
        filepath (str | Path): Path to JSON file
        target_dict (dict): Dictionary to update
        lock (asyncio.Lock): Lock to synchronize with lock
    """
    async with lock:
        dumped_dictionary = json.dumps(target_dict, indent=4, ensure_ascii=False)
        async with aiofiles.open(filepath, mode='w') as f:
            await f.write(dumped_dictionary)


STICKERS = defaultdict(list)
USER_STICKER_SETS = defaultdict(list)
UNIQUE_STICKER_SETS = set()


@dispatcher.message(CommandStart())
async def start_handler(message: Message, bot: Bot) -> None:
    """
    Handles start command
    """
    await message.answer('Привет! Я бот простой: ты мне — стикер, я тебе — стикер\n\n'
                         'Все стикеры, которые у меня есть, — от других пользователей, '
                         'поэтому я не обещаю, что все они будут приличными 😁️️️️\n\n'
                         'И давай по умолчанию считать, что все изображённые на стикерах люди, – иноагенты. '
                         'А то неудобно получается')
    if len(STICKERS) > 0:
        random_emoji = choice(list(STICKERS.keys()))
        random_sticker = choice(STICKERS[random_emoji])
        await message.answer('Я начну')
        await bot.send_sticker(chat_id=message.chat.id, sticker=random_sticker)


@dispatcher.message(Command('stats'))
async def stats_handler(message: Message) -> Message:
    """
    Sends generalized statistics
    """
    total_stickers = len(list(chain(*STICKERS.values())))
    message_text = (f'Стикеров в коллекции: {total_stickers}\nВсего сетов: {len(UNIQUE_STICKER_SETS)}\n'
                    f'Сетов, которые я узнал о тебя: {len(USER_STICKER_SETS[str(message.from_user.id)])}\n\n'
                    f'Как-то так 😁️️')
    return await message.answer(message_text)


@dispatcher.message()
async def message_handler(message: Message, bot: Bot) -> Message:
    """
    Handles any incoming message
    """
    sticker_from_message = message.sticker
    if sticker_from_message is None:
        return await message.reply('Мы так не договаривались, где стикер?')

    sticker_set = await bot.get_sticker_set(sticker_from_message.set_name)
    # Save sticker set
    if sticker_set is not None and sticker_set.name not in UNIQUE_STICKER_SETS:
        USER_STICKER_SETS[str(message.from_user.id)].append(sticker_set.name)
        await save_json_data(settings.BASE_DIR / 'data' / 'stickers.json', STICKERS, stickers_lock)
        UNIQUE_STICKER_SETS.add(sticker_set.name)
        await save_json_data(settings.BASE_DIR / 'data' / 'users.json', USER_STICKER_SETS, users_lock)

        for stick in sticker_set.stickers:
            STICKERS[stick.emoji].append(stick.file_id)

    # Find sticker in response
    matching_stickers = [stick for stick in STICKERS[sticker_from_message.emoji] if stick != sticker_from_message.file_id]
    if len(matching_stickers) == 0:
        return await message.reply('Переиграл и уничтожил, мне нечего сказать!')
    random_sticker = choice(matching_stickers)
    return await bot.send_sticker(chat_id=message.chat.id, sticker=random_sticker)


async def main():
    global STICKERS, USER_STICKER_SETS, UNIQUE_STICKER_SETS

    await load_json_data(settings.BASE_DIR / 'data' / 'stickers.json', STICKERS)
    logger.info(f'Loaded stickers from JSON file: {len(STICKERS)}')
    await load_json_data(settings.BASE_DIR / 'data' / 'users.json', USER_STICKER_SETS)
    logger.info(f'Loaded users from JSON file: {len(USER_STICKER_SETS)}')

    UNIQUE_STICKER_SETS = set(chain(*USER_STICKER_SETS.values()))
    logger.info(f'Collected {len(UNIQUE_STICKER_SETS)} sticker sets on start')

    await dispatcher.start_polling(BOT)


if __name__ == '__main__':
    asyncio.run(main())