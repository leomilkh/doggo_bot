!pip install python-telegram-bot==20.5 requests nest_asyncio --quiet

import logging
import requests
import nest_asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

nest_asyncio.apply()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def get_random_dog():
    url = "https://random.dog/woof.json"
    response = requests.get(url).json()
    while response['url'].endswith(('.mp4', '.webm')):
        response = requests.get(url).json()
    return response['url']

def main_keyboard():
    keyboard = [
        [InlineKeyboardButton("start", callback_data='start')],
        [InlineKeyboardButton("another doggo", callback_data='another')],
        [InlineKeyboardButton("stop", callback_data='stop')]
    ]
    return InlineKeyboardMarkup(keyboard)

def photo_keyboard():
    keyboard = [
        [InlineKeyboardButton("another doggo", callback_data='another')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "hi! i`ll send you a random doggo picture with every click 🐶",
        reply_markup=main_keyboard()
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data in ['start', 'another']:
        dog_url = get_random_dog()
        await query.message.reply_photo(dog_url, caption="here`s your doggo 🐶")
    elif query.data == 'stop':
        await query.message.reply_text("ok, enough for today 🛑")

async def main():
    TOKEN = "your_token_here"  
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("bot is activated...")
    await app.run_polling()

import asyncio
asyncio.get_event_loop().run_until_complete(main())

