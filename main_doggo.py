!pip install python-telegram-bot==20.5 requests --quiet

import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def get_random_dog():
    url = "https://random.dog/woof.json"
    response = requests.get(url).json()
    # Убедимся, что это изображение (не видео)
    while response['url'].endswith(('.mp4', '.webm')):
        response = requests.get(url).json()
    return response['url']

def main_keyboard():
    keyboard = [
        [InlineKeyboardButton("start", callback_data='start')],
        [InlineKeyboardButton("stop", callback_data='stop')],
        [InlineKeyboardButton("another doggo", callback_data='another')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "hi! i'll send you a random picture of a dog 🐶",
        reply_markup=main_keyboard()
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'start':
        dog_url = get_random_dog()
        await query.message.reply_photo(dog_url, caption="here`s your doggo 🐶")
    elif query.data == 'another':
        dog_url = get_random_dog()
        await query.message.reply_photo(dog_url, caption="here`s another one 🐶")
    elif query.data == 'stop':
        await query.message.reply_text("ok, enough for today 🛑")

async def main():
    TOKEN = "your_token_here"

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("bot activated...")
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
