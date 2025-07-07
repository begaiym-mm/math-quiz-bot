import os
import json
import base64
import gspread
import requests
import schedule
import time
from datetime import datetime
from telegram import Bot
from oauth2client.service_account import ServiceAccountCredentials

# === Load environment variables ===
TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
SHEET_NAME = os.getenv("SHEET_NAME")

# === Authorize Google Sheets ===
def load_gspread_client():
    creds_b64 = os.getenv("GOOGLE_CREDENTIALS")
    creds_json = base64.b64decode(creds_b64).decode("utf-8")
    creds_dict = json.loads(creds_json)
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(creds)

gc = load_gspread_client()
sheet = gc.open(SHEET_NAME).sheet1

bot = Bot(token=TOKEN)

# === Daily quiz sender ===
def send_daily_quiz():
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    records = sheet.get_all_records()

    today_row = next((row for row in records if str(row["date"]) == today_str), None)

    if not today_row:
        print("❌ No quiz found for today:", today_str)
        return

    try:
        # Download image
        image_url = today_row["image_url"]
        if "drive.google.com" in image_url:
            file_id = image_url.split("/d/")[1].split("/")[0]
            image_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        img_data = requests.get(image_url).content

        # Optional caption
        caption = today_row.get("caption", "")

        # Send image
        bot.send_photo(chat_id=CHANNEL_ID, photo=img_data, caption=caption)

        # Prepare quiz
        options = [today_row["option1"], today_row["option2"], today_row["option3"], today_row["option4"]]
        correct_index = int(today_row["correct_index"])

        # Send quiz
        bot.send_poll(
            chat_id=CHANNEL_ID,
            question=today_row["question"],
            options=options,
            type='quiz',
            correct_option_id=correct_index,
            is_anonymous=True
        )

        print(f"✅ Quiz sent for {today_str}")

    except Exception as e:
        print(f"❌ Error sending quiz: {e}")

# === Schedule the task daily at 17:18 UTC (22:18 Almaty) ===
schedule.every().day.at("13:40").do(send_daily_quiz)

print("👀 Bot is running and waiting for schedule...")

while True:
    schedule.run_pending()
    time.sleep(30)
