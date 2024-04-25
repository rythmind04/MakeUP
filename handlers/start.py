from aiogram import Bot
from aiogram.types import Message
from keyboards.register import register_keyboard
from keyboards.profile_kb import profile_kb
from utils.database import Database
import os

async def get_start(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    users = db.select_user_id(message.from_user.id)
    if (users):
        await bot.send_message(message.from_user.id, f'Здравствуйте {users.user_name}!', reply_markup=profile_kb)
    else:
        await bot.send_message(message.from_user.id, f'Добро пожаловать в наш салон красоты \n'
                                                 f'Бот поможет записаться к нам на любые услуги', reply_markup=register_keyboard)