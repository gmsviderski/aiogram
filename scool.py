import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command


API_TOKEN = '7017604403:AAGJP0_CL2Fz9Yu8B0sqrrxZjwCH-W4YrRQ'

# Создаем объект бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command('tuesday_schedule'))
async def tuesday_schedule(message: Message):
    response = (
        "*Вторник:*\n"
        "```"
        "08:00 - 09:30: Химия\n"
        "09:40 - 11:10: География\n"
        "```"
    )
    await message.answer(response, parse_mode="Markdown")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())