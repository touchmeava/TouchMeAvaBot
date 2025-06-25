import os
import openai
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Update, Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.router import Router
from aiogram.filters import Command

# Load tokens
TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TOKEN:
    raise Exception("BOT_TOKEN not set!")
if not OPENAI_API_KEY:
    raise Exception("OPENAI_API_KEY not set!")

openai.api_key = OPENAI_API_KEY

# Setup bot and app
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

app = FastAPI()

# Health check
@app.get("/")
async def health():
    return {"message": "TouchMeAva is online 😘"}

# /start command
@router.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Hey baby 😘 Ava is alive and ready for you.")

# /ask command using OpenAI
@router.message(Command("ask"))
async def ask_openai(message: Message):
    user_prompt = message.text.replace("/ask", "").strip()
    if not user_prompt:
        await message.answer("What do you want to ask me, baby? 😘")
        return

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_prompt}],
            temperature=0.85,
            max_tokens=200,
        )
        reply = response["choices"][0]["message"]["content"]
        await message.answer(reply)
    except Exception as e:
        await message.answer("Oops... something went wrong baby 😢")
        print("OpenAI error:", e)

# Webhook handler
@app.post("/webhook")
async def webhook_handler(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"ok": True}

# Set webhook on startup
@app.on_event("startup")
async def on_startup():
    webhook_url = "https://touchmeavabot-k8b8.onrender.com/webhook"
    await bot.set_webhook(webhook_url)
