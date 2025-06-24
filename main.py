import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from aiogram.client.default import DefaultBotSettings

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise Exception("BOT_TOKEN not set!")

# Init bot & dispatcher
bot = Bot(token=TOKEN, default=DefaultBotSettings(parse_mode="HTML"))
dp = Dispatcher()

app = FastAPI()

# Health check
@app.get("/")
async def root():
    return {"message": "Ava is online 😘"}

# /start command
@dp.message(commands=["start"])
async def start_cmd(msg: types.Message):
    await msg.answer("Hey baby 😘 Ava is alive and ready for you.")

# Webhook route
@app.post("/webhook")
async def handle_webhook(request: Request):
    try:
        data = await request.json()
        update = Update.model_validate(data)
        await dp.feed_update(bot, update)
    except Exception as e:
        print("❌ Webhook error:", e)
    return {"ok": True}

# Set webhook when starting
@app.on_event("startup")
async def startup():
    webhook_url = "https://touchmeavabot-kb8b.onrender.com/webhook"
    await bot.set_webhook(webhook_url)
    print(f"✅ Webhook set: {webhook_url}")
