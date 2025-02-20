import logging
import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import Message
from aiogram.filters import Command
# Из своего файла импортирую TOKEN и ADMIN_ID
from api import TOKEN, ADMIN_ID

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создание бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Словарь для хранения ID пользователей
users = {}

@router.message(Command("reply"))
async def reply_message(message: Message):
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
        await bot.send_message(user_id, f"Admindan javob: {reply_text}")
        await message.reply("Javob yuborildi.")
    except Exception as e:
        await message.reply(f"Jo'natishda xatolik: {e}")

@router.message(lambda message: not message.text.startswith("/"))  # Игнорируем команды
async def forward_message(message: Message):
    user = message.from_user
    users[user.id] = user.username  # Сохраняем ID и username пользователя
    text = f"Xabar jo\'natuvchisi: @{user.username or 'Без username'} (ID: {user.id}):\n{message.text}"
    await bot.send_message(ADMIN_ID, text)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
