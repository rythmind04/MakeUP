import asyncio
import os

from aiogram import Bot, Dispatcher, F
from dotenv import load_dotenv
from utils.commands import set_commands
from handlers.start import get_start
from state.regist import RegisterState
from handlers.regist import start_register, register_name, register_phone, register_email
from aiogram.filters import Command

load_dotenv()

token = os.getenv('TOKEN')
admin_id = os.getenv('ADMIN_ID')

bot = Bot(token=token, parse_mode='HTML')
dp = Dispatcher()

async def start_bot(bot: Bot):
    await bot.send_message(admin_id, text='Запущен бот')

dp.startup.register(start_bot)
dp.message.register(get_start, Command(commands='start'))

#Регистрация
dp.message.register(start_register, F.text == 'Регистрация')
dp.message.register(register_name, RegisterState.regName)
dp.message.register(register_phone, RegisterState.regPhone)

async def start():
    await set_commands(bot)
    try:
        await dp.start_polling(bot, skip_updates=True)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())