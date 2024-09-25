import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from gtts import gTTS
from googletrans import Translator
from config import TOKEN


DIRECTORY_NAME = "img"

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()

@dp.message(F.photo)
async def foto(message: Message):
    # Проверяем, существует ли директория
    if not os.path.exists(DIRECTORY_NAME):
        # Если не существует, создаем её
        os.mkdir(DIRECTORY_NAME)
    await bot.download(message.photo[-1], destination=f'img/{message.photo[-1].file_id}.jpg')
    await message.answer('Фото сохранено')

@dp.message(Command('voice'))
async def voice(message: Message):
    tts = gTTS(text='Вам пришло голосовое сообщение', lang='ru')
    tts.save('voice.ogg')
    audio = FSInputFile('voice.ogg')
    await  bot.send_voice(message.chat.id, audio)
    os.remove('voice.ogg')

# Обработчик команды /start
@dp.message(Command('start'))
async def start(message: Message):
    await message.answer("Привет! Отправьте мне любой текст, и я переведу его на английский язык")

@dp.message(Command('help'))
async def help_bot(message: Message):
    await message.answer("Этот бот умеет выполнять команды: \n /start \n /help \n /voice")

# Обработчик всех текстовых сообщений
@dp.message(F.text)
async def translate_message(message: Message):
    original_text = message.text
    translated = translator.translate(original_text, dest='en')
    await message.answer(translated.text)




async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
