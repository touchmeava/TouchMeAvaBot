import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from aiogram.fsm.storage.memory import MemoryStorage

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set!")

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())

app = FastAPI()


@app.get("/")
async def health():
    return {"message": "TouchMeAva is alive 😘"}


@dp.message(commands={"start"})
async def handle_start(message: types.Message):
    await message.answer("Hey baby 😘 Ava is alive and ready for you.")


@app.post("/webhook")
async def webhook_handler(request: Request):
    try:
        data = await request.json()
        update = Update.model_validate(data)
        await dp.feed_update(bot, update)
    except Exception as e:
        print("Webhook error:", e)
    return {"ok": True}


@app.on_event("startup")
async def on_startup():
    webhook_url = "https://touchmeavabot-k8b8.onrender.com/webhook"
    await bot.set_webhook(webhook_url)
    print(f"✅ Webhook set to: {webhook_url}")
