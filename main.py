from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import logging
import json
from datetime import datetime
from typing import List
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Constants
TOKEN = os.getenv('TOKEN')
BOT_USERNAME = os.getenv('BOT_USERNAME')
GROUP_CHAT_ID = os.getenv('GROUP_CHAT_ID')
WEBSITE_URL = os.getenv('WEBSITE_URL')

# Initialize logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Track sent messages
bot_message_ids: List[int] = []

# File to store message timestamps
LOG_FILE = 'message_log.json'

# Initialize the log file if it doesn't exist
def initialize_log():
    try:
        with open(LOG_FILE, 'x') as file:
            json.dump([], file)
    except FileExistsError:
        pass

initialize_log()

# Function to log message timestamps
def log_message_timestamp(timestamp):
    with open(LOG_FILE, 'r+') as file:
        data = json.load(file)
        data.append(timestamp)
        file.seek(0)
        json.dump(data, file)

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text('Hello there! Thanks for chatting with me!!!')
    bot_message_ids.append(msg.message_id)
    log_message_timestamp(datetime.now().isoformat())

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text('For help, you can follow our Discord channel!')
    bot_message_ids.append(msg.message_id)
    log_message_timestamp(datetime.now().isoformat())

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text('Customize')
    bot_message_ids.append(msg.message_id)
    log_message_timestamp(datetime.now().isoformat())

async def sentiment_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = ' '.join(context.args)
    if not text:
        msg = await update.message.reply_text('Usage: /sentiment <text>')
        bot_message_ids.append(msg.message_id)
        log_message_timestamp(datetime.now().isoformat())
        return

    sentiment = analyzer.polarity_scores(text)
    if sentiment['compound'] >= 0.05:
        mood = 'positive'
    elif sentiment['compound'] <= -0.05:
        mood = 'negative'
    else:
        mood = 'neutral'

    response = f"Mood: {mood}\nScores: {sentiment}"
    msg = await update.message.reply_text(response)
    bot_message_ids.append(msg.message_id)
    log_message_timestamp(datetime.now().isoformat())

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    try:
        for message_id in bot_message_ids:
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        await update.message.reply_text('Chat cleared!')
        bot_message_ids.clear()
    except Exception as e:
        logger.error(f"Failed to delete message: {e}")

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    if len(context.args) < 1:
        msg = await update.message.reply_text('Usage: /broadcast <message>')
        bot_message_ids.append(msg.message_id)
        log_message_timestamp(datetime.now().isoformat())
        return

    message = ' '.join(context.args)
    try:
        # Send the message to the group chat
        msg = await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=message)

        # Pin the message in the group chat
        await context.bot.pin_chat_message(chat_id=GROUP_CHAT_ID, message_id=msg.message_id)

        # Notify the user that the message has been broadcasted and pinned successfully
        await update.message.reply_text('Message broadcasted and pinned successfully!')

        # Add the message ID to the list of bot message IDs
        bot_message_ids.append(msg.message_id)
        log_message_timestamp(datetime.now().isoformat())
    except Exception as e:
        logger.error(f'Failed to send broadcast message: {e}')
        msg = await update.message.reply_text(f'Failed to send message: {e}')
        bot_message_ids.append(msg.message_id)
        log_message_timestamp(datetime.now().isoformat())

async def website_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Visit our website: {WEBSITE_URL}')
    log_message_timestamp(datetime.now().isoformat())

# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()
    if any(greeting in processed for greeting in ['hello', 'hi', 'hey', 'heya']):
        return 'Hey there!'
    if any(question in processed for question in ['how are you', 'how are you doing', 'how are you doin']):
        return 'I am good, thank you! How can I assist you today?'
    if any(gm in processed for gm in ['gm', 'good morning']):
        return 'Good morning!'
    if any(gn in processed for gn in ['good night', 'gn']):
        return 'Good night!'
    if any(thanks in processed for thanks in ['thank you', 'thanks']):
        return 'You’re welcome!'
    return "I'm not sure how to respond to that."

# Responding to user contacting our bot
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    message_type: str = update.message.chat.type
    text: str = update.message.text
    logger.info(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    logger.info('Bot:', response)
    msg = await update.message.reply_text(response)
    bot_message_ids.append(msg.message_id)
    log_message_timestamp(datetime.now().isoformat())

async def send_dm_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    if len(context.args) < 2:
        msg = await update.message.reply_text('Usage: /send <username> <message>')
        bot_message_ids.append(msg.message_id)
        log_message_timestamp(datetime.now().isoformat())
        return
    username = context.args[0]
    message = ' '.join(context.args[1:])
    try:
        user_id = await username_to_user_id(username)
        await context.bot.send_message(chat_id=user_id, text=message)
        msg = await update.message.reply_text('Message sent!')
        bot_message_ids.append(msg.message_id)
        log_message_timestamp(datetime.now().isoformat())
    except Exception as e:
        logger.error(f'Failed to send DM: {e}')
        msg = await update.message.reply_text(f'Failed to send message: {e}')
        bot_message_ids.append(msg.message_id)
        log_message_timestamp(datetime.now().isoformat())

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f'Update {update} caused error {context.error}')

async def username_to_user_id(username: str) -> int:
    bot = Bot(token=TOKEN)
    chat = await bot.get_chat(username)
    return chat.id

if __name__ == '__main__':
    logger.info('Starting bot...')
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('send', send_dm_command))
    app.add_handler(CommandHandler('sentiment', sentiment_command))
    app.add_handler(CommandHandler('clear', clear_command))
    app.add_handler(CommandHandler('broadcast', broadcast_command))
    app.add_handler(CommandHandler('website', website_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error)
    logger.info('Polling...')
    app.run_polling(poll_interval=3)
