import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Проверяем, указан ли токен бота в переменных окружения
if not TOKEN:
    raise ValueError("Не указан токен бота. Добавьте его в переменные окружения.")

# Настраиваем логирование для отладки и мониторинга работы бота
logging.basicConfig(filename = r"D:\Python\Scripts\Telegram\First bot\logs.log" ,level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаём экземпляры бота и диспетчера с указанием хранения состояний
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

logger.info("Бот успешно инициализирован.")

@dp.message(CommandStart())  # Обработчик команды /start
async def start_handler(message: Message):
    """
    Функция обрабатывает команду /start и отправляет приветственное сообщение.
    """
    logger.info(f"Получена команда /start от пользователя {message.from_user.id}")
    await message.answer("Привет! Отправь мне любой текст, и я переверну его.")

@dp.message()  # Обработчик текстовых сообщений
async def reverse_text(message: Message):
    """
    Функция принимает текстовое сообщение от пользователя,
    переворачивает его и отправляет обратно.
    """
    text = message.text.strip()  # Убираем лишние пробелы
    logger.info(f"Получено сообщение от {message.from_user.id}: {text}")

    if not text:  # Проверяем, не пустое ли сообщение
        logger.warning(f"Пользователь {message.from_user.id} отправил пустое сообщение.")
        await message.reply("Пожалуйста, отправьте непустое сообщение.")
        return

    reversed_text = text[::-1]  # Переворачиваем строку
    logger.info(f"Ответ пользователю {message.from_user.id}: {reversed_text}")
    await message.reply(reversed_text)  # Отправляем пользователю результат

async def main():
    """
    Основная функция, запускающая бота.
    """
    logger.info("Бот запущен и готов к обработке сообщений.")
    await dp.start_polling(bot, shutdown_timeout=5)  # Запускаем обработку событий с тайм-аутом завершения

if __name__ == "__main__":
    # Запускаем асинхронный цикл для работы бота
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")

"""
Инструкции по запуску бота:
1. Установите зависимости:
   pip install aiogram python-dotenv

2. Создайте файл .env в корневой папке и добавьте строку:
   BOT_TOKEN=ваш_токен_здесь

3. Запустите бота командой:
   python bot.py
"""