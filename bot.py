 
import os
import random
import schedule
import time
from telegram import Bot
from telegram.error import TelegramError


# Получение переменных окружения
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Проверка на наличие токена и канала
if not TOKEN or not CHANNEL_ID:
    print("❌ BOT_TOKEN или CHANNEL_ID не заданы в Heroku → Settings → Config Vars")
    exit(1)

bot = Bot(token=TOKEN)

# Список викторин
quiz_data = [
    {
        "question": "Сколько планет в Солнечной системе?",
        "options": ["7", "8", "9", "10"],
        "correct_option_id": 1
    },
    {
        "question": "Что такое H2O?",
        "options": ["Кислород", "Водород", "Вода", "Азот"],
        "correct_option_id": 2
    }
]

# Функция отправки викторины
def send_daily_quiz():
    quiz = random.choice(quiz_data)
    try:
        bot.send_poll(
            chat_id=CHANNEL_ID,
            question=quiz["question"],
            options=quiz["options"],
            type='quiz',
            correct_option_id=quiz["correct_option_id"],
            is_anonymous=True
        )
        print("✅ Куиз отправлен.")
    except TelegramError as e:
        print(f"❌ Ошибка отправки: {e}")
    except Exception as ex:
        print(f"❌ Другая ошибка: {ex}")

# Временная отправка тест-сообщения (можно убрать позже)
try:
    bot.send_message(chat_id=CHANNEL_ID, text="✅ Бот запущен. Это тестовое сообщение.")
    print("✅ Тестовое сообщение отправлено.")
except TelegramError as e:
    print(f"❌ Ошибка при тестовой отправке: {e}")

send_daily_quiz()
# Расписание: 22:18 по Алматы = 17:18 UTC
# schedule.every().day.at("17:18").do(send_daily_quiz)

print("👀 Бот работает, ждёт расписания...")

# Главный цикл
while True:
    schedule.run_pending()
    time.sleep(30)
