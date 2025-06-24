import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from aiogram.client.default import DefaultBotSettings
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from aiogram.filters import Command

# Setup
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise Exception("BOT_TOKEN not set!")

bot = Bot(token=TOKEN, default=DefaultBotSettings(parse_mode="HTML"))
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

app = FastAPI()

@app.get("/")
async def health():
    return {"message": "TouchMeAva is online 😘"}

# Start command handler
@router.message(Command("start"))
async def start_cmd(msg: types.Message):
    await msg.answer("Hey baby 😘 Ava is alive and ready for you.")

# Webhook handler
@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
        update = Update.model_validate(data)
        await dp.feed_update(bot, update)
        print("✅ Update handled")
    except Exception as e:
        print("❌ Error:", e)
    return {"ok": True}

# Set webhook on startup
@app.on_event("startup")
async def on_startup():
    url = "https://touchmeavabot-k8b8.onrender.com/webhook"
    await bot.set_webhook(url)
    print(f"✅ Webhook set to: {url}")
