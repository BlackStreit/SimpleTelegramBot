import os  # Модуль для работы с переменными окружения и файловой системой
import logging  # Модуль для ведения логирования
import asyncio  # Модуль для работы с асинхронным программированием
from aiogram import Bot, Dispatcher, types  # Импорт основных классов aiogram для работы с ботом
from aiogram.types import Message, BotCommand  # Импорт типов сообщений и команд бота
from aiogram.filters import CommandStart, Command  # Импорт фильтров для обработки команд
from aiogram.fsm.storage.memory import MemoryStorage  # Импорт хранилища состояний (в памяти)
from dotenv import load_dotenv  # Модуль для загрузки переменных окружения из .env файла
from datetime import datetime  # Модуль для работы с датой и временем

# Настройка логирования: запись событий в файл logs.log
logging.basicConfig(filename=r"D:\Python\Scripts\Telegram\First bot\logs.log", level=logging.INFO)
logger = logging.getLogger(__name__)  # Получение логгера с именем текущего модуля

# Загрузка переменных окружения из .env файла
load_dotenv()
# Получение токена бота из переменных окружения
TOKEN = os.getenv("BOT_TOKEN")

# Проверка наличия токена
if TOKEN:
    logger.info(f"{datetime.now()} Токен бота получен")  # Логирование успешного получения токена
else:
    logger.error(f"{datetime.now()} Не указан токен бота. Добавьте его в переменные окружения.")  # Ошибка если токен отсутствует
    raise ValueError("Не указан токен бота. Добавьте его в переменные окружения.")  # Выбрасывание исключения

# Создание экземпляра бота и диспетчера
bot = Bot(token=TOKEN)  # Инициализация бота с переданным токеном
dp = Dispatcher(storage=MemoryStorage())  # Инициализация диспетчера с хранилищем состояний в памяти

# Функция установки команд бота
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запустить бота"),  # Команда для старта бота
        BotCommand(command="info", description="Вести информацию об авторе"),  # Команда для информации об авторе
        BotCommand(command="uppercase", description="Преобразовать текст в верхний регистр")  # Команда для преобразования текста
    ]
    await bot.set_my_commands(commands)  # Установка списка команд в боте

# Обработчик команды /start
@dp.message(CommandStart())
async def start_message(message: Message):
    print(f"Получена команда /start от пользователя {message.from_user.id}")
    logger.info(f"{datetime.now()} Получена команда /start от пользователя {message.from_user.id}")  # Логирование получения команды
    await message.answer("Привет. Напиши мне сообщение, а я его переверну")  # Ответ пользователю

# Обработчик команды /info
@dp.message(Command("info"))
async def info_command(message: Message):
    print(f"Получена команда info от пользователя {message.from_user.id}")
    logger.info(f"{datetime.now()} Получена команда info от пользователя {message.from_user.id}")  # Логирование получения команды
    await message.answer("Бот разработан KaiHere")  # Ответ пользователю с информацией об авторе

# Обработчик команды /uppercase
@dp.message(Command("uppercase"))
async def text_to_upper(message: Message):
    text = message.text.replace("/uppercase", "").strip()  # Удаляем команду из текста и убираем пробелы
    if not text:  # Проверяем, если сообщение пустое
        print("Пустое сообщение")
        logger.warning(f"{datetime.now()} Пустое сообщение от пользователя {message.from_user.id}")  # Логирование предупреждения
        await message.answer("Пожалуйста, введи сообщение")  # Просим пользователя ввести сообщение
        return
    uptext = text.upper()  # Преобразуем текст в верхний регистр
    logger.info(f"Преобразованный текст в верхний регистр для {message.from_user.id}: {uptext}")  # Логируем преобразование
    await message.reply(uptext)  # Отправляем пользователю преобразованный текст

# Обработчик сообщений (по умолчанию)
@dp.message()
async def reverse_message(message: Message):
    text = message.text.strip()  # Убираем лишние пробелы
    
    if not text:  # Проверяем, если сообщение пустое
        print("Пустое сообщение")
        logger.warning(f"{datetime.now()} Пустое сообщение от пользователя {message.from_user.id}")  # Логируем предупреждение
        await message.answer("Пожалуйста, введи сообщение")  # Просим пользователя ввести сообщение
        return
    
    rev_text = text[::-1]  # Переворачиваем строку
    await message.reply(rev_text)  # Отправляем пользователю перевернутое сообщение

# Функция завершения работы бота
async def shutdown():
    print("Пока-пока")
    logger.info(f"{datetime.now()} Бот выключается")  # Логирование выключения бота
    await bot.session.close()  # Закрытие сессии бота

# Основная функция запуска бота
async def main():
    await set_commands(bot)  # Устанавливаем команды бота
    try:
        print("Бот запускается...")
        logger.info(f"{datetime.now()} Бот включается")  # Логирование запуска
        await dp.start_polling(bot, shutdown_timeout=5)  # Запуск лонг-поллинга с таймаутом 5 секунд при завершении
    finally:
        await shutdown()  # Вызов функции завершения

# Запуск скрипта
if __name__ == '__main__':
    try:
        asyncio.run(main())  # Запуск асинхронного event-loop для бота
    except Exception as e:
        print(f"Ошибка {e}")
        logger.error(f"{datetime.now()} Ошибка {e}")  # Логирование ошибки
