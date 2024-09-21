import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import sqlite3
import logging

TOKEN = 'Ваш токен'

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()


def init_db():
    conn = sqlite3.connect('school_data.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade TEXT NOT NULL)
        ''')
    conn.commit()
    conn.close()


init_db()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Как тебя зовут?")
    await state.set_state(Form.name)


@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)


@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer("В каком классе учишься?")
    await state.set_state(Form.grade)


@dp.message(Form.grade)
async def city(message: Message, state: FSMContext):
    await state.update_data(grade =message.text)
    user_data = await state.get_data()
    conn = sqlite3.connect('school_data.db')
    cursor = conn.cursor()
    cursor.execute('''
       INSERT INTO students (name, age, grade) VALUES (?, ?, ?)''',
                (user_data['name'], user_data['age'], user_data['grade']))
    conn.commit()
    conn.close()

    await message.answer(f"Тебя зовут {user_data['name']}. \nТебе {user_data['age']} лет. \nТы учишься в {user_data['grade']} классе.")

    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())