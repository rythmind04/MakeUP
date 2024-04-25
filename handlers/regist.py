from aiogram.types import Message
from aiogram import Bot
from aiogram.fsm.context import FSMContext
from state.regist import RegisterState
import re
import os
from utils.database import Database

async def start_register(message:Message, state:FSMContext):
    db = Database(os.getenv('DATABASE_NAME'))
    users = db.select_user_id(message.from_user.id)
    if(users):
        await message.answer(f'{users.user_name} \nВы уже зарегистрированы')
    else:
        await message.answer(f'Давайте начнем регистрацию \nСкажите как вас зовут?')
        await state.set_state(RegisterState.regName)

async def register_name(message:Message, state:FSMContext):
    await message.answer(f'Приятно познакомится {message.text}\n'
                         f'Теперь укажите ваш номер телефона \n'
                         f'Формат телефона должен быть: +7xxxxxxxxxx \n'
                         f'⚠️ Прошу проверить формат номера ⚠️')
    await state.update_data(regname=message.text)
    await state.set_state(RegisterState.regPhone)

async def register_phone(message: Message, state: FSMContext, bot: Bot):
    if re.findall("^\+?[7][-\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$", message.text):
        await state.update_data(regphone=message.text)
        await bot.send_message(message.from_user.id, "Отлично! Теперь укажите ваш email.")
        await state.set_state(RegisterState.regEmail)
    else:
        await bot.send_message(message.from_user.id, "Номер указан в неправильном формате")


async def register_email(message: Message, state: FSMContext, bot: Bot):
    if re.match(r"[^@]+@[^@]+\.[^@]+", message.text):
        await state.update_data(regemail=message.text)
        reg_data = await state.get_data()
        reg_name = reg_data.get("regname")
        reg_phone = reg_data.get("regphone")
        reg_email = reg_data.get("regemail")
        msg = f"Приятно познакомиться {reg_name} \n\n Телефон - {reg_phone} \n\n Email - {reg_email}"
        await bot.send_message(message.from_user.id, msg)
        db = Database(os.getenv("DATABASE_NAME"))
        db.add_user(reg_name, reg_phone, message.from_user.id, reg_email)
        await state.clear()
    else:
        await bot.send_message(message.from_user.id, "Email указан в неправильном формате")