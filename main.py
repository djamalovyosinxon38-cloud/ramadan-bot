import os
import asyncio
import logging
from aiohttp import web
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8855415202:AAFZeFxLTWwB5QI8XQaVuIOiLyQMPjpa9hE"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- TUGMALAR ---
BTN_TODAY = "📅 Bugun"
BTN_TOMORROW = "📅 Ertaga"
BTN_MONTH = "📆 To'liq taqvim"
BTN_REGION = "🇺🇿 Mintaqa"
BTN_DUA = "🤲 Duo"

main_buttons = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=BTN_TODAY), KeyboardButton(text=BTN_TOMORROW)],
        [KeyboardButton(text=BTN_MONTH)],
        [KeyboardButton(text=BTN_REGION), KeyboardButton(text=BTN_DUA)]
    ],
    resize_keyboard=True
)

region_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Тошкент", callback_data="region_1"),
            InlineKeyboardButton(text="Андижон", callback_data="region_2")
        ]
    ]
)

# --- 30 KUNLIK TAQVIM BAZASI ---
TAQVIM_BAZASI = {
    "2026-08-15": {"kun": 1, "sahar": "04:10", "iftor": "19:25"},
    "2026-08-16": {"kun": 2, "sahar": "04:11", "iftor": "19:24"},
    "2026-08-17": {"kun": 3, "sahar": "04:12", "iftor": "19:22"},
    "2026-08-18": {"kun": 4, "sahar": "04:14", "iftor": "19:21"},
    "2026-08-19": {"kun": 5, "sahar": "04:15", "iftor": "19:19"},
    "2026-08-20": {"kun": 6, "sahar": "04:16", "iftor": "19:18"},
    "2026-08-21": {"kun": 7, "sahar": "04:17", "iftor": "19:16"},
    "2026-08-22": {"kun": 8, "sahar": "04:18", "iftor": "19:15"},
    "2026-08-23": {"kun": 9, "sahar": "04:20", "iftor": "19:13"},
    "2026-08-24": {"kun": 10, "sahar": "04:21", "iftor": "19:12"},
    "2026-08-25": {"kun": 11, "sahar": "04:22", "iftor": "19:10"},
    "2026-08-26": {"kun": 12, "sahar": "04:23", "iftor": "19:08"},
    "2026-08-27": {"kun": 13, "sahar": "04:24", "iftor": "19:07"},
    "2026-08-28": {"kun": 14, "sahar": "04:25", "iftor": "19:05"},
    "2026-08-29": {"kun": 15, "sahar": "04:26", "iftor": "19:03"},
    "2026-08-30": {"kun": 16, "sahar": "04:28", "iftor": "19:02"},
    "2026-08-31": {"kun": 17, "sahar": "04:29", "iftor": "19:00"},
    "2026-09-01": {"kun": 18, "sahar": "04:30", "iftor": "18:58"},
    "2026-09-02": {"kun": 19, "sahar": "04:31", "iftor": "18:57"},
    "2026-09-03": {"kun": 20, "sahar": "04:32", "iftor": "18:55"},
    "2026-09-04": {"kun": 21, "sahar": "04:33", "iftor": "18:53"},
    "2026-09-05": {"kun": 22, "sahar": "04:34", "iftor": "18:52"},
    "2026-09-06": {"kun": 23, "sahar": "04:35", "iftor": "18:50"},
    "2026-09-07": {"kun": 24, "sahar": "04:36", "iftor": "18:48"},
    "2026-09-08": {"kun": 25, "sahar": "04:37", "iftor": "18:46"},
    "2026-09-09": {"kun": 26, "sahar": "04:38", "iftor": "18:45"},
    "2026-09-10": {"kun": 27, "sahar": "04:39", "iftor": "18:43"},
    "2026-09-11": {"kun": 28, "sahar": "04:40", "iftor": "18:41"},
    "2026-09-12": {"kun": 29, "sahar": "04:42", "iftor": "18:39"},
    "2026-09-13": {"kun": 30, "sahar": "04:43", "iftor": "18:38"},
}

# --- HANDLERLAR ---
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        f"Ассалому алайкум <b>{message.from_user.first_name}</b>!\n\n"
        "<b>Рамазон ойи муборак бўлсин!</b>\n\n"
        "Сизга қайси минтақа бўйича маълумот керак?",
        reply_markup=region_inline,
        parse_mode="HTML"
    )

@dp.callback_query(F.data.startswith("region_"))
async def inline_callback(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer(
        "<b>Рамазон тақвими</b>\n\nҚуйидагилардан бирини танланг 👇",
        reply_markup=main_buttons,
        parse_mode="HTML"
    )
    await call.answer()

@dp.message(F.text == BTN_TODAY)
async def calendar_today(message: types.Message):
    bugun_sana = datetime.now().strftime("%Y-%m-%d")
    if bugun_sana in TAQVIM_BAZASI:
        m = TAQVIM_BAZASI[bugun_sana]
        matn = (
            f"📅 <b>Бугун: {bugun_sana}</b>\n\n"
            f"🌙 Рамазоннинг <b>{m['kun']}-куни</b>\n"
            f"🌅 Саҳарлик: <b>{m['sahar']}</b>\n"
            f"🌇 Ифторлик: <b>{m['iftor']}</b>"
        )
    else:
        matn = "❌ Бугунги тақвим маълумотлари топилмади."
    await message.answer(matn, parse_mode="HTML")

@dp.message(F.text == BTN_TOMORROW)
async def calendar_tomorrow(message: types.Message):
    ertaga_sana = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    if ertaga_sana in TAQVIM_BAZASI:
        m = TAQVIM_BAZASI[ertaga_sana]
        matn = (
            f"📅 <b>Эртага: {ertaga_sana}</b>\n\n"
            f"🌙 Рамазоннинг <b>{m['kun']}-куни</b>\n"
            f"🌅 Саҳарлик: <b>{m['sahar']}</b>\n"
            f"🌇 Ифторлик: <b>{m['iftor']}</b>"
        )
    else:
        matn = "❌ Эртанги тақвим маълумотлари топилмади."
    await message.answer(matn, parse_mode="HTML")

@dp.message(F.text == BTN_MONTH)
async def calendar_month(message: types.Message):
    text = "📆 <b>Рамазон ойининг тўлиқ тақвими (Тошкент вақти):</b>\n\n"
    text += "<code>Кун | Саҳар  | Ифтор </code>\n"
    text += "<code>-----------------------</code>\n"
    for sana, m in TAQVIM_BAZASI.items():
        text += f"<code>{m['kun']:02d}-кун | {m['sahar']} | {m['iftor']}</code>\n"
    await message.answer(text, parse_mode="HTML")

@dp.message(F.text == BTN_DUA)
async def select_dua(message: types.Message):
    dua_text = (
        "🤲 <b>Рамазон ойи дуолари</b>\n\n"
        "🌅 <b>Саҳарлик (Оғиз ёпиш) дуоси:</b>\n"
        "<i>«Навайту ан асума совма шаҳри Рамазона минал фажри илал мағриби, холисан лиллаҳи таъала. Аллоҳу акбар.»</i>\n\n"
        "<b>Ma'nosi:</b> Рамазон ойининг рўзасини субҳдан то кун ботгунча холис Аллоҳ учун тутишни ният қилдим.\n\n"
        "------------------------------------\n\n"
        "🌇 <b>Ифторлик (Оғиз очиш) дуоси:</b>\n"
        "<i>«Аллоҳумма лака сумту ва бика аманту ва ъалайка таваккалту ва ъала ризқика афтарту, фағфирли йа Ғоффару ма қоддамту ва ма аххорту.»</i>\n\n"
        "<b>Ma'nosi:</b> Эй Аллоҳ, ушбу рўзамни Сенинг учун тутдим, Сенга иймон келтирдим, Сенга таваккал қилдим ва Сенинг ризқинг билан оғиз очдим. Эй гуноҳларни кечирувчи Зот, менинг аввалги ва кейинги гуноҳларимни мағфират қилгин."
    )
    await message.answer(dua_text, parse_mode="HTML")

@dp.message(F.text == BTN_REGION)
async def select_region(message: types.Message):
    await message.answer("Минтақани ўзгартириш:", reply_markup=region_inline)

async def handle(request):
    return web.Response(text="Bot is active!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Web server {port}-portda ishga tushdi")

async def main():
    await asyncio.gather(
        start_web_server(),
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    asyncio.run(main())
