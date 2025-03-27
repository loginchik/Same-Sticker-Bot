import asyncio
from aiogram import Bot, Dispatcher
from .settings import settings


bot = Bot(token=settings.BOT_TOKEN)
dispatcher = Dispatcher()


async def main():
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())