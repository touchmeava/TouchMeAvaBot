import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from aiogram.client.default import DefaultBotSettings
from aiogram import Router
from aiogram.filters import Command

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise Exception("BOT_TOKEN is not set!")

# Init bot and dispatcher
bot = Bot(token=TOKEN, default=DefaultBotSettings(parse_mode="HTML"))
dp = Dispatcher()
router = Router()
dp.include_router(router)

app = FastAPI()

@app.get("/")
async def health():
    return {"message": "TouchMeAva is online 😘"}

@router.message(Command("start"))
async def start_cmd(msg: types.Message):
    await msg.answer("Hey baby 😘 Ava is alive and ready for you.")

@app.post("/webhook")
async def handle_webhook(request: Request):
    try:
        data = await request.json()
        update = Update.model_validate(data)
        await dp.feed_update(bot, update)
    except Exception as e:
        print("❌ Webhook error:", e)
    return {"ok": True}

@app.on_event("startup")
async def on_startup():
    webhook_url = "https://touchmeavabot-k8b8.onrender.com/webhook"
    await bot.set_webhook(webhook_url)
    print(f"✅ Webhook set: {webhook_url}")
