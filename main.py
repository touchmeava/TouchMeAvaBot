import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Update
from aiogram.client.default import DefaultBotSettings
from aiogram.router import Router

# Load bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise Exception("❌ BOT_TOKEN not set!")

# Create bot and dispatcher
bot = Bot(token=BOT_TOKEN, default=DefaultBotSettings(parse_mode="HTML"))
dp = Dispatcher()
router = Router()
dp.include_router(router)

# FastAPI app
app = FastAPI()

# Health check
@app.get("/")
async def health():
    return {"message": "TouchMeAva is online 😘"}

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

# Telegram /start command handler
@router.message(F.text == "/start")
async def start_cmd(msg: types.Message):
    await msg.answer("Hey baby 😘 Ava is alive and ready for you.")

# Set webhook on startup
@app.on_event("startup")
async def startup():
    webhook_url = "https://touchmeavabot-k8b8.onrender.com/webhook"
    await bot.set_webhook(webhook_url)
    print(f"✅ Webhook set: {webhook_url}")
