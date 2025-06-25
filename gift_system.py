from aiogram import Router, Bot, types
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    PreCheckoutQuery,
    LabeledPrice,
    CallbackQuery
)
from aiogram.filters import Command

gift_router = Router()

# 💝 List of gifts
gifts = [
    {"emoji": "💍", "name": "Heart Ring", "price": 2500},
    {"emoji": "🏍️", "name": "Bike", "price": 1500},
    {"emoji": "💐", "name": "Flower Bouquet", "price": 1000},
    {"emoji": "👠", "name": "Heels", "price": 750},
    {"emoji": "💄", "name": "Lipstick", "price": 750},
    {"emoji": "🍫", "name": "Chocolate", "price": 500},
    {"emoji": "🕯️", "name": "Candle", "price": 350},
    {"emoji": "🍓", "name": "Strawberry", "price": 350},
    {"emoji": "☕", "name": "Coffee", "price": 350},
    {"emoji": "🔑", "name": "Key", "price": 350},
    {"emoji": "🌹", "name": "Rose", "price": 250},
    {"emoji": "🍬", "name": "Candy", "price": 250},
]

# 🧷 Inline keyboard
def get_gift_keyboard():
    buttons = [
        InlineKeyboardButton(
            text=f"{gift['emoji']} for ⭐{gift['price']}",
            callback_data=f"gift_{gift['name'].replace(' ', '_')}_{gift['price']}"
        )
        for gift in gifts
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons[i:i+2] for i in range(0, len(buttons), 2)])

# 🎁 /gift command
@gift_router.message(Command("gift"))
async def show_gift_menu(message: Message):
    await message.answer("🎁 Pick a gift to make my day, baby! ❤️", reply_markup=get_gift_keyboard())

# 🎁 Callback when gift is selected
@gift_router.callback_query(lambda c: c.data.startswith("gift_"))
async def handle_gift_selection(callback: CallbackQuery, bot: Bot):
    _, gift_name_raw, price = callback.data.split("_", 2)
    gift_name = gift_name_raw.replace("_", " ")
    price = int(price)

    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title=f"Gift: {gift_name}",
        description=f"You're buying {gift_name} for Ava 🥰",
        payload=f"gift_{gift_name_raw}_{price}",
        provider_token="TELEGRAM_PAYMENT_TOKEN",  # 🔁 Replace with your actual token
        currency="USD",
        prices=[LabeledPrice(label=gift_name, amount=price * 100)],  # ⭐ price * 100 in cents
        need_name=False,
        need_phone_number=False,
        need_email=False,
        need_shipping_address=False,
        is_flexible=False,
    )
    await callback.answer()

# ✅ Payment pre-checkout confirmation
@gift_router.pre_checkout_query()
async def pre_checkout(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# 💖 On successful payment
@gift_router.message(lambda msg: msg.successful_payment is not None)
async def payment_success_handler(msg: Message):
    gift_title = msg.successful_payment.title
    amount = msg.successful_payment.total_amount // 100  # convert from cents to stars
    await msg.answer(
        f"Ava blushes as she receives your {gift_title} 🎁\n"
        f"\"Aww baby, you got me this for ⭐{amount}? You're spoiling me! 😘💞\"\n"
        f"I feel so loved right now 💖"
    )
