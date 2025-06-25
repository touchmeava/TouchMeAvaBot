from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
from aiogram.filters import Command

stars_router = Router()

# ✅ Example list of gifts with Star cost
gifts = [
    {"emoji": "💍", "name": "Heart Ring", "price": 25},
    {"emoji": "🏍️", "name": "Bike", "price": 15},
    {"emoji": "💐", "name": "Bouquet", "price": 10},
    {"emoji": "🌹", "name": "Rose", "price": 5},
    {"emoji": "🍬", "name": "Candy", "price": 2},
]

# ✅ Price mapping for Telegram invoice (in cents)
PRICE_MAPPING = {
    "heart_ring": LabeledPrice(label="Heart Ring", amount=2500),
    "bike": LabeledPrice(label="Bike", amount=1500),
    "bouquet": LabeledPrice(label="Bouquet", amount=1000),
    "rose": LabeledPrice(label="Rose", amount=500),
    "candy": LabeledPrice(label="Candy", amount=200),
}

# ✅ Generate inline keyboard
def get_star_gift_keyboard():
    buttons = [
        InlineKeyboardButton(
            text=f"{gift['emoji']} {gift['name']} – ⭐{gift['price']}",
            callback_data=f"star_gift_{gift['name'].lower().replace(' ', '_')}_{gift['price']}"
        )
        for gift in gifts
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=[buttons[i:i+2] for i in range(0, len(buttons), 2)]
    )

# ✅ /gift command
@stars_router.message(Command("gift"))
async def send_gift_list(message: types.Message):
    await message.answer(
        "🎁 Pick a gift to send me with Telegram Stars:\n\n"
        "Tap any gift below and confirm the payment ⭐",
        reply_markup=get_star_gift_keyboard()
    )

# ✅ Callback when a gift is selected
@stars_router.callback_query(lambda c: c.data.startswith("star_gift_"))
async def process_star_gift(callback: types.CallbackQuery):
    _, _, gift_name_raw, price_str = callback.data.split("_", 3)
    gift_key = gift_name_raw.lower()
    gift_name = gift_key.replace("_", " ")

    # Optional: Check if price exists in map
    if gift_key not in PRICE_MAPPING:
        await callback.answer("This gift is not available right now.")
        return

    await callback.answer()

    await callback.message.answer(
        f"Ava gasps! 😳 You sent her a {gift_name} worth ⭐{price_str}!\n"
        f"\"You're making me melt, baby... I feel so special 💖\""
    )
