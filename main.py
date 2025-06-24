import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer("Hey love, I’m Ava – your AI girlfriend 💋. Talk to me anytime 💖")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
