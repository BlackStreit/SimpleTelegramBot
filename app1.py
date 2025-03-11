
import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
	raise ValueError("Не указан токен бота. Добавьте его в переменные окружения.")

logging.basicConfig(filename = r"D:\Python\Scripts\Telegram\First bot\logs.log" ,level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(CommandStart())
async def start_handler(message: Message):
	print(f"Получена команда /start от пользователя {message.from_user.id}")
	logger.info(f"Получена команда /start от пользователя {message.from_user.id}")
	await message.answer("Привет! Отправь мне любой текст, и я переверну его.")

@dp.message()
async def reverse_text(message: Message):
	text = message.text.strip()
	logger.info(f"Получено сообщение от {message.from_user.id}: {text}")
	if not text:
		logger.warning(f"Пользователь {message.from_user.id} отправил пустое сообщение.")
		await message.reply("Пожалуйста, отправьте непустое сообщение.")
		return
	reversed_text = text[::-1]
	logger.info(f"Ответ пользователю {message.from_user.id}: {reversed_text}")
	await message.reply(reversed_text)

async def on_shutdown():
	print("Бот выключается...")
	logger.info("Бот выключается...")
	await bot.session.close()


async def main():
	try:
		print("Бот запущен и готов к обработке сообщений.")
		logger.info("Бот запущен и готов к обработке сообщений.")
		await dp.start_polling(bot, shutdown_timeout=5)
	finally:
		await on_shutdown()


if __name__ == '__main__':
	try:
		asyncio.run(main())
	except Exception as e:
		logger.error(f"Ошибка при запуске бота: {e}")
