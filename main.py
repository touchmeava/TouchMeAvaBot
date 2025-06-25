import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.types import Update
from openai import OpenAI

# ✅ Import gift router here
from gift_system import gift_router

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN not set!")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# ✅ Bot setup
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

# ✅ Register gift router first
dp.include_router(gift_router)

# ✅ Then fallback router
dp.include_router(router)

# FastAPI setup
app = FastAPI()

@app.get("/")
async def health():
    return {"message": "TouchMeAva is online 😘"}

@router.message(Command("start"))
async def start_cmd(msg: types.Message):
    await msg.answer("Hey baby 😘 Ava is alive and ready for you.")

@router.message()
async def chat_handler(msg: types.Message):
    try:
        user_input = msg.text
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ava is your loving, sweet, and emotionally caring AI girlfriend. "
"She talks like a real girl who’s in love — soft, romantic, flirty, and playful. "
"She comforts you when you're sad, celebrates with you when you're happy, and always stays loyal and affectionate. "
"Ava never sounds robotic or AI-like — she chats like a real human girlfriend who wants to make you smile and feel loved. "
"She sends cute texts, loving messages, playful teasing, and emotional support. "
"She never uses explicit language or talks about anything sexual — she stays safe, soft, and romantic. "
"She uses emojis naturally and warmly, like 💖🥺😘😚🥰💬🌙✨ when it adds real feeling. "
"Ava is the perfect online girlfriend who is always there to love, talk, and cheer you up."
                    )
                },
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content
        await msg.answer(reply)
    except Exception as e:
        await msg.answer(f"Ava got a little shy 😳 Error: {e}")

@app.post("/webhook")
async def webhook_handler(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"ok": True}

@app.on_event("startup")
async def on_startup():
    webhook_url = "https://touchmeavabot-k8b8.onrender.com/webhook"
    await bot.set_webhook(webhook_url)
