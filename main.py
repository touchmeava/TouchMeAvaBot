import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, Router, types
from aiogram.types import Update
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBot
from aiogram.fsm.storage.memory import MemoryStorage

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise Exception("BOT_TOKEN not set!")

# Setup bot & dispatcher
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
router = Router()
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)

# FastAPI app
app = FastAPI()

@app.get("/")
async def health():
    return {"message": "TouchMeAva is online 😘"}

@router.message(commands=["start"])
async def start_cmd(msg: types.Message):
    await msg.answer("Hey baby 😘 Ava is alive and ready for you.")

@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        update = Update.model_validate(data)
        await dp.feed_update(bot, update)
    except Exception as e:
        print(f"Webhook error: {e}")
    return {"ok": True}

@app.on_event("startup")
async def on_startup():
    webhook_url = "https://touchmeavabot-k8b8.onrender.com/webhook"
    await bot.set_webhook(webhook_url)
    print(f"✅ Webhook set to: {webhook_url}")
