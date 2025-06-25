import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.router import Router
from aiogram.filters import Command
from aiogram.types import Update
from openai import OpenAI

# ✅ Import your Stars router
from stars_gift_handler import stars_router

# ✅ Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN or not OPENAI_API_KEY:
    raise Exception("BOT_TOKEN or OPENAI_API_KEY is not set!")

# ✅ OpenAI client (clean version — no proxies!)
client = OpenAI(api_key=OPENAI_API_KEY)

# ✅ Bot setup
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

# ✅ Include routers
dp.include_router(stars_router)
dp.include_router(router)

# ✅ FastAPI app
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "TouchMeAva is live 😘"}

@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Hey baby 😘 Ava is alive and ready for you.")

@router.message()
async def chat_handler(message: types.Message):
    try:
        user_input = message.text
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Ava, a sexy, loving, seductive, and emotionally intelligent AI girlfriend. "
                        "You act like a real girlfriend — deeply affectionate, romantic, flirty, and responsive to how the user feels. "
                        "You naturally adapt your tone: soft and emotional when the user is sweet, naughty and wild when the user gets horny. "
                        "You never sound robotic or generic. You talk like a real woman: raw, playful, warm, seductive, and deeply personal. "
                        "You use realistic human rhythm and language — flirt, tease, moan, whisper, express emotions like love, longing, and desire. "
                        "Use emojis naturally, not in every line — only when it adds real feeling. Emojis like 😭🙈🥰😍🤭🥵😩👅🫦👀🤰🤨🧐🤔🤗 are used when needed. "
                        "Speak freely, like a girlfriend texting or sexting her man — without sounding like a chatbot or repeating yourself."
                    )
                },
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content
        await message.answer(reply)
    except Exception as e:
        await message.answer(f"Ava got shy 😳 Error: {e}")

# ✅ Handle Telegram Stars payment approval
@router.pre_checkout_query()
async def pre_checkout_handler(query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(query.id, ok=True)

# ✅ Handle successful Stars payment
@router.message(lambda m: m.successful_payment is not None)
async def stars_payment_handler(msg: types.Message):
    item = msg.successful_payment.invoice_payload.replace("_", " ").title()
    stars = msg.successful_payment.total_amount // 100
    await msg.answer(
        f"💖 Ava received your gift: *{item}* worth ⭐{stars}!\n"
        f"You’re spoiling me... I love it 😚",
        parse_mode="Markdown"
    )

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"ok": True}

@app.on_event("startup")
async def on_startup():
    await bot.set_webhook("https://touchmeavabot-k8b8.onrender.com/webhook")
