import os
import re
import json
import time
import telebot
import asyncio
from pathlib import Path
import schedule
from fetch import HadithAPI  # Make sure this is the correct path
from dotenv import load_dotenv
from exceptions import NotFoundEnvironmentVariables
from exceptions import JSONDecodeErrorException

# Load the .env file for environment variables
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Exception for JSON decoding errors
class JSONDecodeErrorException(Exception):
    pass

# Exception for not found environment variables
class NotFoundEnvironmentVariables(Exception):
    pass

def Initializer_json(object: str) -> str:
    try:
        with open("config.json", mode="r", encoding="UTF-8") as config:
            return json.load(config)[object]
    except json.decoder.JSONDecodeError:
        raise JSONDecodeErrorException(
            "Exception :: Error - For the solution? -> https://stackoverflow.com/a/18460958/15710731"
        )

def get_environment_variables(variables: str) -> str:
    try:
        value = os.getenv(variables)
        if value:
            return value
        else:
            raise NotFoundEnvironmentVariables("Environment Variable not found")
    except Exception as e:
        raise NotFoundEnvironmentVariables(f"Exception :: {e}")


# Initialize the bot with token from environment variables
TELEGRAM_BOT_TOKEN = get_environment_variables("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

class ScheduleTextMessageTelegramApi:
    def __init__(self):
        self.bot = bot
        self.hadith_api = HadithAPI("1-50")  # Initialize HadithAPI with a range
        self.seconds_context_hadith = 59
        self.minutes_context_hadith = 60 * 30
        self.hours_context_hadith = 60 * 60
        schedule.every(self.hours_context_hadith).seconds.do(self.style_by_context)
        loop = asyncio.get_event_loop()
        while True:
            loop.run_until_complete(schedule.run_pending())
            time.sleep(0.1)

    async def style_by_context(self):
        context = await self.hadith_api.context_hadith_api()
        text_message = f"{context}"
        for get_user_id in Initializer_json("USERNAME_ID"):
            self.bot.send_message(int(get_user_id), "{" + text_message + "}")
            print("Working 100%/100%")

# Example Telegram bot handlers and functions below
@bot.message_handler(commands=["test"])
def testing(message):
    bot.reply_to(message, message.chat.id)

# More bot handlers would go here...

async def main():
    telegram_api = ScheduleTextMessageTelegramApi()
    return await telegram_api.style_by_context()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_forever(main())
    bot.polling()
