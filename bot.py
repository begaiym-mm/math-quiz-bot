def send_daily_quiz():
    try:
        bot.send_message(chat_id=CHANNEL_ID, text="🔔 Привет! Бот работает!")
        print("✅ Сообщение отправлено.")
    except TelegramError as e:
        print(f"❌ Ошибка: {e}")
