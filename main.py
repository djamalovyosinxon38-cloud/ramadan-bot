import os
import logging
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

# Logging
logging.basicConfig(level=logging.INFO)

# TELEGRAM BOT TOKENINGIZNI SHU YERGA YOZING:
BOT_TOKEN = "8855415202:AAG20sGgXpB-aZXPZat1Ohyw8mJ84LCbWZI"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- BOT BUYRUQLARI (HANDLERS) ---
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Assalomu alaykum! Ramadan botga xush kelibsiz!")

# --- RENDER PORT XATOLIGINI TUZATISH UCHUN VEB-SERVER ---
async def handle_ping(request):
    return web.Response(text="Bot is running live 24/7!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logging.info(f"Dummy Web Server running on port {port}")

# --- MAIN RUNNER ---
async def main():
    # 1. Render port xatosi bermasligi uchun veb-serverni yurgizamiz
    await start_web_server()
    # 2. Telegram botni polling rejimida ishga tushiramiz
    logging.info("Starting Telegram Bot polling...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
