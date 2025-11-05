import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command

TOKEN = "8376787921:AAGk999p5aTPurkT8ukrx6YwV4QOdKmVFGI"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    web_app = WebAppInfo(url="https://gcbudgethelper.onrender.com/")
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Open Dashboard", web_app=web_app)]
        ],
        resize_keyboard=True
    )
    await message.answer(
        "Click the button below to open your dashboard 👇",
        reply_markup=keyboard
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("Bot is starting...")
    asyncio.run(main())
