from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

def print_chat_id(update: Update, context: CallbackContext):
    chat = update.effective_chat
    print(f"🆔 chat.id = {chat.id}")

updater = Updater(token=TOKEN, use_context=True)
updater.dispatcher.add_handler(MessageHandler(Filters.all, print_chat_id))

updater.start_polling()

 
