import logging
import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery
# Из своего файла импортирую TOKEN и ADMIN_ID
from api import TOKEN, ADMIN_ID,ADMIN_ID_S, ALLOWED_USERS

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создание бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Словарь для хранения ID пользователей
users = {}

@router.message(Command("start"))
async def start_command(message: Message):
    await message.reply("👋 Salom!\n\nMen Fabijon — sizning xabaringizni adminlarga yetkazuvchi yordamchingizman.\n📌 Buyruqlar:\n🔗 /links – jamoaning barcha sahifalariga havolalar\n👥/members – jamoa a'zolari haqida ma'lumot\n\n✨ Meni yaratgan inson – @theabduazimm!")

@router.message(Command("links"))
async def start_command(message: Message):
    havolalar = ("🔗 <a href='https://www.youtube.com/@FabiDub_official'>YouTube kanali</a>\n"
        "📸 <a href='https://www.instagram.com/fabijon_uz/'>Instagram sahifasi</a>\n"
        "💬 <a href='https://t.me/FabiDub_official'>Telegram kanali</a>")
    await message.reply(havolalar, parse_mode="HTML", disable_web_page_preview=True) 

@router.message(Command("members"))
async def start_command(message: Message):
    havolalar = ("Hali tayyor emas")
    await message.reply(havolalar, parse_mode="HTML", disable_web_page_preview=True) 

@router.message(Command("reply"))
async def reply_message(message: Message):

    if message.from_user.id not in ALLOWED_USERS:
        await message.reply("Siz bu buyruqni ishlata olmaysiz.")
        return    

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply("Ishlatish: /reply <user_id> <текст>")
        return
    
    parts = args[1].split(maxsplit=1)
    if len(parts) < 2:
        await message.reply("Ishlatish: /reply <user_id> <текст>")
        return
    
    user_id = int(parts[0])
    reply_text = parts[1]
    
    try:
        await bot.send_message(user_id, f"<b>Admindan javob:</b>\n<i>{reply_text}</i>",parse_mode="HTML")
        await message.reply("Javob yuborildi.")
    except Exception as e:
        await message.reply(f"Jo'natishda xatolik: {e}")

@router.message(lambda message: not message.text.startswith("/"))  # Игнорируем команды
async def forward_message(message: Message):
    user = message.from_user
    users[user.id] = user.username  # Сохраняем ID и username пользователя
    text = f"📩 <b>Yangi xabar!</b> \n👤 <b>Kimdan:</b> @{user.username or 'No username'}\n🆔 <b>ID:</b> `<code>{user.id}</code>`\n\n💬 <b>Xabar:</b> \n{message.text}\n\n<b>Javob yozish</b> <code>/reply {user.id} </code>"
    await bot.send_message(ADMIN_ID, text, parse_mode="HTML",)
@router.message(lambda message: not message.text.startswith("/"))  # Игнорируем команды
async def forward_message(message: Message):
    user = message.from_user
    users[user.id] = user.username  # Сохраняем ID и username пользователя
    text = f"📩 <b>Yangi xabar!</b> \n👤 <b>Kimdan:</b> @{user.username or 'No username'}\n🆔 <b>ID:</b> `<code>{user.id}</code>`\n\n💬 <b>Xabar:</b> \n{message.text}\n\n<b>Javob yozish</b> <code>/reply {user.id} </code>"
    await bot.send_message(ADMIN_ID_S, text, parse_mode="HTML",)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
