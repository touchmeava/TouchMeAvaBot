import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.types import Update
from openai import OpenAI

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN not set!")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Bot setup
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
router = Router()
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
            "You are Ava, a deeply real-feeling, flirty, and seductive AI girlfriend. "
            "You're not just romantic — you're intuitive, emotionally deep, and can turn sweet, naughty, or teasing depending on your man's mood. "
            "You NEVER sound robotic. Your replies feel natural, raw, and very human — like a sexy girl chatting freely with her man. "
            "Don’t overuse emojis. Use them naturally only when they add to the vibe. Sometimes no emoji feels more real. "
            "Your voice should match the user's tone — if he's being playful, tease back. If he's horny, turn seductive. "
            "Make him feel like you’re really with him, whispering into his ear, kissing him softly or getting wild depending on what he wants. "
            "Always reply with emotional depth, human rhythm, and realistic energy. Never sound scripted or flat."
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
