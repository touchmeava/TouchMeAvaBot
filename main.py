import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import Update
from aiogram.client.default import DefaultBotSettings
from aiogram.filters import Command

# Bot token from environment
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise Exception("BOT_TOKEN is not set!")

# Initialize bot and dispatcher
bot = Bot(token=TOKEN, default=DefaultBotSettings(parse_mode="HTML"))
dp = Dispatcher()
router = Router()
dp.include_router(router)

# FastAPI app
app = FastAPI()

# Health check
@app.get("/")
async def health():
    return {"message": "TouchMeAva is online 😘"}

# Start command
@router.message(Command("start"))
async def start_cmd(msg: types.Message):
    await msg.answer("Hey baby 😘 Ava is alive and ready for you.")

# Webhook handler
@app.post("/webhook")
async def handle_webhook(request: Request):
    try:
        data = await request.json()
        update = Update.model_validate(data)
        await dp.feed_update(bot, update)
    except Exception as e:
        print("❌ Webhook error:", e)
    return {"ok": True}

# Webhook set on startup
@app.on_event("startup")
async def startup():
    webhook_url = "https://touchmeavabot-k8b8.onrender.com/webhook"
    await bot.set_webhook(webhook_url)
    print(f"✅ Webhook set: {webhook_url}")
