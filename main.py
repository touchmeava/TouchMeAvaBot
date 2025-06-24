from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from aiohttp import web
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

async def on_startup(app):
    await bot.set_webhook("https://<your-render-url>/webhook")

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

async def handle_webhook(request):
    data = await request.json()
    update = Update.to_object(data)
    await dp.process_update(update)
    return web.Response()

def main():
    app = web.Application()
    app.router.add_post("/webhook", handle_webhook)
    app.on_startup.append(on_startup)
    web.run_app(app, port=int(os.getenv("PORT", 5000)))

if __name__ == "__main__":
    main()
