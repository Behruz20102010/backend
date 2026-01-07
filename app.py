import asyncio
import random
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, InlineKeyboardMarkup, InlineKeyboardButton,
    LabeledPrice, PreCheckoutQuery, CallbackQuery
)

TOKEN = "8277869771:AAGUXjrUh_7oLYbEavCkSWBVIpAPd4lOWF8"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Barcha narxlar (Stars)
PRICES = {
    "play_1": {"stars": 1, "emoji": "⭐"},
    "play_5": {"stars": 5, "emoji": "⭐"},
    "play_10": {"stars": 10, "emoji": "⭐"},
    "play_15": {"stars": 15, "emoji": "⭐"},
    "play_25": {"stars": 25, "emoji": "⭐⭐"},
    "play_50": {"stars": 50, "emoji": "⭐⭐"},
    "play_100": {"stars": 100, "emoji": "⭐⭐⭐"},
    "play_200": {"stars": 200, "emoji": "⭐⭐⭐"},
    "play_300": {"stars": 300, "emoji": "⭐⭐⭐"},
    "play_500": {"stars": 500, "emoji": "⭐⭐⭐⭐"},
    "play_750": {"stars": 750, "emoji": "⭐⭐⭐⭐"},
    "play_1000": {"stars": 1000, "emoji": "⭐⭐⭐⭐⭐"}
}

# Gift yutuqlari (sovg'alar va ehtimollik)
GIFT_PRIZES = [
    {"prize": "nothing", "chance": 25, "emoji": "😢", "text": "Afsuski, hech narsa", "stars": 0},
    {"prize": "teddy", "chance": 20, "emoji": "🧸", "text": "Teddy!", "stars": 0},
    {"prize": "roza_25", "chance": 15, "emoji": "🌹", "text": "25 Stars + Roza!", "stars": 25},
    {"prize": "roza_teddy", "chance": 7, "emoji": "🌹🧸", "text": "Roza + Teddy!", "stars": 0},
    {"prize": "tort_50", "chance": 2, "emoji": "🎂", "text": "50 Stars + Tort!", "stars": 50},
    {"prize": "tort_teddy", "chance": 1, "emoji": "🎂🧸", "text": "Tort + Teddy!", "stars": 0},
    {"prize": "diamond", "chance": 1, "emoji": "💎", "text": "DIAMOND JACKPOT!", "stars": 0}
]

def get_random_prize():
    """Random yutuq tanlash"""
    # Barcha ehtimolliklarni yig'ish
    total_chance = sum(p["chance"] for p in GIFT_PRIZES)
    rand = random.randint(1, total_chance)
    
    current = 0
    for prize in GIFT_PRIZES:
        current += prize["chance"]
        if rand <= current:
            return prize
    
    return GIFT_PRIZES[0]  # Default

async def play_gift_animation(message: Message, stars_paid: int):
    """Gift ochish animatsiyasi"""
    # 1. Gift ochilmoqda...
    msg = await message.answer("🎁 Gift ochilmoqda...")
    await asyncio.sleep(1)
    
    # 2. Animatsiya
    animations = ["🎁", "🎀", "🎊", "✨", "🎉"]
    for emoji in animations:
        await msg.edit_text(f"{emoji} Gift ochilmoqda...")
        await asyncio.sleep(0.5)
    
    # 3. Yutuqni aniqlash
    prize = get_random_prize()
    
    # 4. Natijani ko'rsatish
    result_text = (
        f"{prize['emoji']} <b>{prize['text']}</b>\n\n"
        f"💰 To'langan: {stars_paid} ⭐\n"
    )
    
    # Yutuqni ko'rsatish
    if prize['prize'] == "nothing":
        result_text += f"🎁 Yutuq: Hech narsa 😢\n\n"
        result_text += f"<i>Yana harakat qiling! Omad keyingi safar! 🍀</i>"
    elif prize['prize'] == "teddy":
        result_text += f"🎁 Yutuq: Teddy 🧸\n\n"
        result_text += f"<b>Ajoyib! Siz Teddy yutdingiz! 🎉</b>"
    elif prize['prize'] == "roza_25":
        result_text += f"🎁 Yutuq: 25 ⭐ + Roza 🌹\n\n"
        result_text += f"<b>Zo'r! 25 Stars va Roza sizniki! 💐</b>"
    elif prize['prize'] == "roza_teddy":
        result_text += f"🎁 Yutuq: Roza 🌹 + Teddy 🧸\n\n"
        result_text += f"<b>Qoyil! Ikkala sovg'a ham sizniki! 🎊</b>"
    elif prize['prize'] == "tort_50":
        result_text += f"🎁 Yutuq: 50 ⭐ + Tort 🎂\n\n"
        result_text += f"<b>Super! 50 Stars va Tort! 🎉🎉</b>"
    elif prize['prize'] == "tort_teddy":
        result_text += f"🎁 Yutuq: Tort 🎂 + Teddy 🧸\n\n"
        result_text += f"<b>Ajoyib! Premium sovg'alar! 🏆🎊</b>"
    elif prize['prize'] == "diamond":
        result_text += f"🎁 Yutuq: DIAMOND 💎💎💎\n\n"
        result_text += f"<b>🏆 MEGA JACKPOT! DIAMOND YUTDINGIZ! 🏆</b>\n"
        result_text += f"<i>Sizga katta tabriklar! 🎉🎊✨</i>"
    
    # Yana o'ynash tugmasi
    play_again_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎮 Yana o'ynash", callback_data="play_again")]
        ]
    )
    
    await msg.edit_text(result_text, reply_markup=play_again_kb, parse_mode="HTML")

@dp.message(F.text == "/start")
async def start(message: Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            # 1-qator: kichik narxlar
            [
                InlineKeyboardButton(text="⭐ 1", callback_data="play_1"),
                InlineKeyboardButton(text="⭐ 5", callback_data="play_5"),
                InlineKeyboardButton(text="⭐ 10", callback_data="play_10"),
            ],
            # 2-qator: o'rta narxlar
            [
                InlineKeyboardButton(text="⭐ 15", callback_data="play_15"),
                InlineKeyboardButton(text="⭐ 25", callback_data="play_25"),
                InlineKeyboardButton(text="⭐ 50", callback_data="play_50"),
            ],
            # 3-qator: katta narxlar
            [
                InlineKeyboardButton(text="⭐⭐ 100", callback_data="play_100"),
                InlineKeyboardButton(text="⭐⭐ 200", callback_data="play_200"),
                InlineKeyboardButton(text="⭐⭐ 300", callback_data="play_300"),
            ],
            # 4-qator: juda katta narxlar
            [
                InlineKeyboardButton(text="⭐⭐⭐ 500", callback_data="play_500"),
                InlineKeyboardButton(text="⭐⭐⭐ 750", callback_data="play_750"),
            ],
            # 5-qator: maksimal
            [
                InlineKeyboardButton(text="⭐⭐⭐⭐⭐ 1000", callback_data="play_1000")
            ]
        ]
    )
    await message.answer(
        "🎮 <b>Gift O'yiniga xush kelibsiz!</b>\n\n"
        "🎁 Qanday o'ynaladi?\n"
        "1️⃣ Narx tanlang\n"
        "2️⃣ To'lov qiling\n"
        "3️⃣ Gift oching va sovg'a oling!\n\n"
        "💰 Narxlar: 1 dan 1000 Stars gacha\n"
        "🎯 Sovg'alar:\n"
        "• 💎 Diamond - MEGA JACKPOT (1%)\n"
        "• 🎂🧸 Tort + Teddy (1%)\n"
        "• 🎂 50 Stars + Tort (2%)\n"
        "• 🌹🧸 Roza + Teddy (7%)\n"
        "• 🌹 25 Stars + Roza (15%)\n"
        "• 🧸 Teddy (20%)\n"
        "• 😢 Afsuski, hech narsa (25%)\n\n"
        "<i>Omad yor bo'lsin! 🍀</i>",
        reply_markup=kb,
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "play_again")
async def play_again(call: CallbackQuery):
    """Yana o'ynash"""
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⭐ 1", callback_data="play_1"),
                InlineKeyboardButton(text="⭐ 5", callback_data="play_5"),
                InlineKeyboardButton(text="⭐ 10", callback_data="play_10"),
            ],
            [
                InlineKeyboardButton(text="⭐ 15", callback_data="play_15"),
                InlineKeyboardButton(text="⭐ 25", callback_data="play_25"),
                InlineKeyboardButton(text="⭐ 50", callback_data="play_50"),
            ],
            [
                InlineKeyboardButton(text="⭐⭐ 100", callback_data="play_100"),
                InlineKeyboardButton(text="⭐⭐ 200", callback_data="play_200"),
                InlineKeyboardButton(text="⭐⭐ 300", callback_data="play_300"),
            ],
            [
                InlineKeyboardButton(text="⭐⭐⭐ 500", callback_data="play_500"),
                InlineKeyboardButton(text="⭐⭐⭐ 750", callback_data="play_750"),
            ],
            [
                InlineKeyboardButton(text="⭐⭐⭐⭐⭐ 1000", callback_data="play_1000")
            ]
        ]
    )
    await call.message.edit_text(
        "🎮 <b>Yana o'ynaymizmi?</b>\n\n"
        "💰 Narxni tanlang:",
        reply_markup=kb,
        parse_mode="HTML"
    )
    await call.answer()

@dp.callback_query(F.data.in_(PRICES.keys()))
async def invoice(call: CallbackQuery):
    # Tanlangan narxni olish
    price_data = PRICES[call.data]
    stars_amount = price_data["stars"]
    emoji = price_data["emoji"]
    
    await bot.send_invoice(
        chat_id=call.from_user.id,
        title=f"🎁 Gift O'yini - {stars_amount} Stars",
        description=f"Gift ochish va yutuq yutish imkoniyati! {stars_amount} {emoji}",
        payload=call.data,
        provider_token="",      # Stars uchun bo'sh
        currency="XTR",         # Telegram Stars
        prices=[LabeledPrice(label=f"{stars_amount} Stars", amount=stars_amount)]
    )
    await call.answer(f"Invoice yuborildi: {stars_amount} ⭐")

@dp.pre_checkout_query()
async def pre_checkout(query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(query.id, ok=True)

@dp.message(F.successful_payment)
async def success(message: Message):
    payment = message.successful_payment
    stars_paid = payment.total_amount
    
    await message.answer(
        f"✅ <b>To'lov muvaffaqiyatli!</b>\n\n"
        f"💰 To'langan: {stars_paid} ⭐\n"
        f"🎁 Gift ochilmoqda...\n\n"
        f"<i>Bir daqiqa...</i>",
        parse_mode="HTML"
    )
    
    # Gift o'yinini boshlash
    await play_gift_animation(message, stars_paid)

async def main():
    print("🚀 Bot ishga tushdi...")
    print("🎮 Gift o'yini aktiv!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())