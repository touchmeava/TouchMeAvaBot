from aiogram import Router, types
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from aiogram.filters import Command

gift_router = Router()

# List of gifts with emoji, name, price (in stars)
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

# Build inline buttons
def get_gift_keyboard():
    buttons = [
        InlineKeyboardButton(
            text=f"{gift['emoji']} for ⭐ {gift['price']}",
            callback_data=f"gift_{gift['name'].replace(' ', '_')}_{gift['price']}"
        )
        for gift in gifts
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons[i:i + 2] for i in range(0, len(buttons), 2)])

# Handle /gift command
@gift_router.message(Command("gift"))
async def gift_command_handler(message: Message):
    await message.answer(
        "🎁 Pick a gift to make Ava smile 😘",
        reply_markup=get_gift_keyboard()
    )

# Handle gift button clicks
@gift_router.callback_query(lambda c: c.data.startswith("gift_"))
async def handle_gift_selection(callback: types.CallbackQuery, bot: types.Bot):
    await callback.answer()
    _, raw_name, raw_price = callback.data.split("_", 2)
    gift_name = raw_name.replace("_", " ")
    gift_price = int(raw_price)

    # Stars payment
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title=f"Gift: {gift_name}",
        description=f"Send Ava a {gift_name} ❤️",
        provider_token="STARS",  # Special token for Telegram Stars (do not change)
        currency="STARS",
        prices=[LabeledPrice(label=gift_name, amount=gift_price)],
        payload=f"gift_{gift_name}"
    )

# Handle successful payment
@gift_router.pre_checkout_query()
async def pre_checkout_handler(query: types.PreCheckoutQuery, bot: types.Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)

@gift_router.message(lambda msg: msg.successful_payment is not None)
async def payment_success_handler(message: Message):
    gift_name = message.successful_payment.invoice_payload.replace("gift_", "")
    amount = message.successful_payment.total_amount
    await message.answer(
        f"💖 Ava received your {gift_name} for ⭐ {amount}!\n"
        f"She hugs you tightly and kisses your cheek 😘\n"
        f"You made her day!"
    )
