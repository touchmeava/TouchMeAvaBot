from aiogram import Router, types
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command

gift_router = Router()

# Gift data
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

# Keyboard builder
def get_gift_keyboard():
    buttons = [
        InlineKeyboardButton(
            text=f"{gift['emoji']} for ⭐ {gift['price']}",
            callback_data=f"gift_{gift['name'].replace(' ', '_')}_{gift['price']}"
        )
        for gift in gifts
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons[i:i + 2] for i in range(0, len(buttons), 2)])

# Command handler
@gift_router.message(Command("gift"))
async def gift_command_handler(message: Message):
    await message.answer(
        "🎁 Pick a gift to make my day! ❤️",
        reply_markup=get_gift_keyboard()
    )

# Button handler
@gift_router.callback_query(lambda c: c.data.startswith("gift_"))
async def gift_selection_handler(callback_query: CallbackQuery):
    _, gift_name_raw, price = callback_query.data.split("_", 2)
    gift_name = gift_name_raw.replace("_", " ")
    price = int(price)

    await callback_query.answer()
    await callback_query.message.answer(
        f"Ava blushes as she receives your {gift_name} 🎁\n"
        f"\"Aww baby, you got me this for ⭐{price}? You're spoiling me! 😘💞\"\n"
        f"I feel so loved right now 💖"
    )
