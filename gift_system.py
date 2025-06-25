from aiogram import Router, types
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice, PreCheckoutQuery, SuccessfulPayment, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram import F

gift_router = Router()

# Gift list
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
            callback_data=f"gift:{gift['name'].replace(' ', '_')}"
        )
        for gift in gifts
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons[i:i + 2] for i in range(0, len(buttons), 2)])

# /gift command
@gift_router.message(Command("gift"))
async def gift_command_handler(message: Message):
    await message.answer("🎁 Pick a gift to make my day! ❤️", reply_markup=get_gift_keyboard())

# Send Stars invoice
async def send_stars_invoice(message: Message, title: str, description: str, price: int):
    await message.answer_invoice(
        title=title,
        description=description,
        payload="gift_payment",
        provider_token="STARS",
        currency="XTR",
        prices=[LabeledPrice(label=title, amount=price)],
        max_tip_amount=0,
    )

# Gift button handler
@gift_router.callback_query(F.data.startswith("gift:"))
async def handle_gift_click(callback_query: CallbackQuery):
    gift_name_raw = callback_query.data.split(":")[1]
    gift_name = gift_name_raw.replace("_", " ")

    gift = next((g for g in gifts if g["name"] == gift_name), None)
    if not gift:
        await callback_query.answer("Gift not found", show_alert=True)
        return

    title = f"{gift['emoji']} {gift['name']}"
    description = f"A sweet gift for Ava: {gift['name']}"
    price = gift['price'] * 100  # in cents

    await send_stars_invoice(callback_query.message, title, description, price)
    await callback_query.answer()

# Handle pre-checkout
@gift_router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    await pre_checkout_q.answer(ok=True)

# Handle payment success
@gift_router.message(F.successful_payment)
async def on_successful_payment(message: Message):
    stars = message.successful_payment.total_amount / 100
    await message.answer(f"Thank you for the ⭐ {stars} stars, my love! 💖")
