from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

# Load environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set in environment variables!")

# Bot setup
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# FastAPI app
app = FastAPI()

# Health check route (optional but recommended)
@app.get("/")
async def root():
    return {"message": "TouchMeAva bot is live!"}

# Webhook handler
@app.post("/webhook")
async def webhook_handler(request: Request):
    try:
        data = await request.json()
        print("Received webhook:", data)  # ✅ For debugging
        update = Update.to_object(data)
        await dp.process_update(update)
    except Exception as e:
        print(f"Webhook error: {e}")
    return {"ok": True}

# Bot command handler
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.reply("Hey cutie 😘 I’m alive and listening to you...")

# Set webhook on startup
@app.on_event("startup")
async def on_startup():
    webhook_url = "https://touchmeavabot-k8b8.onrender.com/webhook"
    await bot.set_webhook(webhook_url)
    print(f"Webhook set to: {webhook_url}")
