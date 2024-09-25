import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
import random
from gtts import gTTS
import os

TOKEN = '7017604403:AAGJP0_CL2Fz9Yu8B0sqrrxZjwCH-W4YrRQ'

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video') # индикация в телеграме загрузки видео
    video = FSInputFile('video.mp4')
    await bot.send_video(message.chat.id, video)

@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile('sample.ogg')
    await message.answer_voice(voice)

@dp.message(Command('doc'))
async def doc(message: Message):
    doc = FSInputFile('TG02.pdf')
    await bot.send_document(message.chat.id, doc)


@dp.message(Command('audio'))
async def audio(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_audio')
    audio = FSInputFile('Ring07.wav')
    await bot.send_audio(message.chat.id, audio)

@dp.message(Command('training'))
async def training(message: Message):
    training_list = [
        "Тренировка 1:\n1. Скручивания: 3 подхода по 15 повторений \n2. Велосипед: 3 подхода по 20 повторений (каждая сторона) \n3. Планка: 3 подхода по 30 секунд",
        "Тренировка 2:\n1. Подъемы ног: 3 подхода по 15 повторений \n2. Русский твист: 3 подхода по 20 повторений (каждая сторона) \n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
        "Тренировка 3:\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений  \n2. Горизонтальные ножницы: 3 подхода по 20 повторений \n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
    ]
    rand_tr = random.choice(training_list)
    await message.answer(f'Это ваша тренировка на сегодня {rand_tr}')
    tts = gTTS(text=rand_tr, lang='ru')
    tts.save('training.ogg')
    audio = FSInputFile('training.ogg')
    await  bot.send_voice(message.chat.id, audio)
    os.remove('training.ogg')

# @dp.message(Command('photo', prefix='@'))
@dp.message('photo')
async def foto(message: Message):
    lst = ['https://e-tapetki.pl/tapetki/duze/194129_dwa-kotki.jpg', 'https://e-tapetki.pl/tapetki/duze/378771_.jpg']
    rand_foto = random.choice(lst)
    await message.answer_photo(photo=rand_foto, caption='это крутая картинка')

@dp.message(F.photo)
async def foto(message: Message):
    lst = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_ansi = random.choice(lst)
    await message.answer(rand_ansi)
    await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg')

@dp.message(F.text == "Что такое ИИ")
async def aitext (message: Message):
    await message.answer("Искуственный интелект")

@dp.message(CommandStart())
async def start_bot(message: Message):
    await message.answer(f'Приветики, {message.from_user.first_name}!')


@dp.message(Command('help'))
async def help_bot(message: Message):
    await message.answer("Этот бот умеет выполнять команды: \n /start \n /help")

#Эхобот, должен быть в конце программы
@dp.message()
async def start_bot(message: Message):
    if message.text.lower() == 'test':
        await message.answer('мы тестируем')


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())