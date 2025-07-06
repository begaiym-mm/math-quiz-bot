import os
import random
import schedule
import time
from telegram import Bot
from telegram.error import TelegramError

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=TOKEN)

quiz_data = [
    {
        "question": "Какой язык программирования используется для Telegram-ботов?",
        "options": ["Python", "HTML", "CSS", "Photoshop"],
        "correct_option_id": 0
    },
    {
        "question": "Сколько дней в високосном году?",
        "options": ["365", "366", "364", "360"],
        "correct_option_id": 1
    }
]

def send_daily_quiz():
    quiz = random.choice(quiz_data)
    try:
        bot.send_poll(
            chat_id=CHANNEL_ID,
            question=quiz["question"],
            options=quiz["options"],
            type='quiz',
            correct_option_id=quiz["correct_option_id"],
            is_anonymous=False
        )
        print("✅ Куиз отправлен.")
    except TelegramError as e:
        print(f"❌ Ошибка отправки: {e}")

schedule.every().day.at("17:18").do(send_daily_quiz)

print("👀 Бот запущен на Heroku")

while True:
    schedule.run_pending()
    time.sleep(30)
