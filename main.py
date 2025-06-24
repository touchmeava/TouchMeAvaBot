from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

# Load environment variable (make sure BOT_TOKEN is set in Render panel)
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Bot setup
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# FastAPI app
app = FastAPI()

# Webhook route
@app.post("/webhook")
async def webhook_handler(request: Request):
    print("✅ Webhook called")  # <-- Add this
    try:
        data = await request.json()
        update = Update.to_object(data)
        await dp.process_update(update)
    except Exception as e:
        print(f"Webhook error: {e}")
    return {"ok": True}

# Command handler
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.reply("Hey cutie 😘 I’m alive and listening to you...")

# Set webhook on startup
@app.on_event("startup")
async def on_startup():
    webhook_url = "https://touchmeavabot-kb8b.onrender.com/webhook"
    await bot.set_webhook(webhook_url)
