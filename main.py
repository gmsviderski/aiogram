import asyncio               # для работы с асинхронными функциями
import aiohttp
from aiogram import Bot, Dispatcher  # Bot для работы с телеграмАПИ Dicpether обработка исходящих сообщений и команд
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

TOKEN = '7017604403:AAGJP0_CL2Fz9Yu8B0sqrrxZjwCH-W4YrRQ'
WEATHER_API_KEY = 'bda4f18c30aa281201fc4ccfa0b9f77c'
WEATHER_CITY = 'Cherepovets'
WEATHER_URL = f'http://api.openweathermap.org/data/2.5/weather?q={WEATHER_CITY}&appid={WEATHER_API_KEY}&units=metric&lang=ru'

bot = Bot(token=TOKEN)
dp = Dispatcher()



async def fetch_weather():
    async with aiohttp.ClientSession() as session:
        async with session.get(WEATHER_URL) as response:
            return await response.json()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я бот прогноза погоды. Используйте /help, чтобы увидеть доступные команды.")

@dp.message(Command('help'))
async def help_bot(message: Message):
    help_text = (
        "Доступные команды:\n"
        "/start - Начать работу с ботом\n"
        "/help - Получить список доступных команд\n"
        "/prognoz - Получить прогноз погоды в Череповце"
    )
    await message.answer(help_text)

@dp.message(Command('prognoz'))
async def send_weather(message: Message):
    weather_data = await fetch_weather()
    if weather_data.get("main"):
        temp = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]
        weather_report = f"Погода в Череповце: {description.capitalize()}.\nТемпература: {temp}°C."
    else:
        weather_report = "Не удалось получить данные о погоде."
    await message.answer(weather_report)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())