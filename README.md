# Telegram Bot with Sentiment Analysis

This project implements a Telegram bot using the `python-telegram-bot` library. The bot includes functionalities such as sentiment analysis, logging messages, broadcasting messages, and handling responses based on simple text analysis.

## Features

- Start and Help commands to interact with the bot
- Sentiment analysis of text using VADER sentiment analysis
- Logging of message timestamps
- Clear chat functionality
- Broadcasting messages to a group chat and pinning them
- Responding to simple text inputs
- Direct messaging users by username

## Requirements

- Python 3.7+
- Telegram Bot Token

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/telegram-bot-with-sentiment-analysis.git
    cd telegram-bot-with-sentiment-analysis
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your environment variables:
    ```env
    TOKEN=your-telegram-bot-token
    BOT_USERNAME=@your_bot_username
    GROUP_CHAT_ID=your-group-chat-id
    WEBSITE_URL=https://your-website.com
    ```

5. Run the bot:
    ```bash
    python bot.py
    ```

## Usage

### Commands

- `/start`: Greets the user.
- `/help`: Provides help information.
- `/custom`: Responds with "Customize".
- `/sentiment <text>`: Analyzes the sentiment of the provided text.
- `/clear`: Clears all messages sent by the bot in the chat.
- `/broadcast <message>`: Sends a broadcast message to the group chat and pins it.
- `/website`: Shares the website URL.
- `/send <username> <message>`: Sends a direct message to the specified user.

### Text Responses

The bot responds to various greetings and common phrases such as:
- Hello, hi, hey, heya
- How are you, how are you doing
- Good morning, gm
- Good night, gn
- Thank you, thanks

## Logging

Message timestamps are logged in `message_log.json`.

### Example

Here's an example of interacting with the bot:
![image](https://github.com/user-attachments/assets/be2c6e6f-9def-47a4-a9af-695287d33874)
![image](https://github.com/user-attachments/assets/141374d4-4d57-49d6-a319-f182d020e015)

