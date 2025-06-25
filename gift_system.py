from aiogram import Router, types, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command

from loader import bot  # make sure this points to your Bot instance

gift_router = Router()

# List of gifts (emoji, name, price in Stars)
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

# Inline keyboard
def get_gift_keyboard():
    buttons = [
        InlineKeyboardButton(
            text=f"{gift['emoji']} for ⭐ {gift['price']}",
            callback_data=f"gift_{gift['name'].replace(' ', '_')}_{gift['price']}"
        )
        for gift in gifts
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons[i:i + 2] for i in range(0, len(buttons), 2)])

# /gift command
@gift_router.message(Command("gift"))
async def gift_command_handler(message: Message):
    await message.answer(
        "🎁 Pick a gift to make my day! ❤️",
        reply_markup=get_gift_keyboard()
    )

# Send Stars payment
async def send_stars_invoice(message: Message, title: str, description: str, amount: int):
    await bot.request_gift_payment(
        user_id=message.from_user.id,
        title=title,
        amount=amount  # amount is in Stars (int only)
    )

# Handle button click
@gift_router.callback_query(F.data.startswith("gift_"))
async def handle_gift_click(callback_query: types.CallbackQuery):
    await callback_query.answer()

    _, gift_name_raw, price = callback_query.data.split("_", 2)
    gift_name = gift_name_raw.replace("_", " ")
    price = int(price)

    # Trigger Telegram Stars flow
    await send_stars_invoice(callback_query.message, gift_name, f"Send {gift_name} to Ava", price)

    await callback_query.message.answer(
        f"Ava blushes as she sees the {gift_name} gift 🎁\n"
        f"\"Aww baby, you trying to spoil me with ⭐{price}? You're too sweet! 😘\"\n"
        f"Waiting for your Stars to shine... ✨"
    )
