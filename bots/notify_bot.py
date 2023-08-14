import time

import telebot
from dotenv import load_dotenv

load_dotenv(".botdata")
bot_token = "5815237536:AAHrKa1tFkJjENSisgKWpMORWgs2OPIhOrc"
chat_id = "-948029729"


def send_message_attempts(msg="nothing passed"):
    def send_message(msg):
        bot = telebot.TeleBot(token=bot_token)
        bot.send_message(
            chat_id=chat_id,
            text=msg
        )

    result = 1
    tries = 55
    while tries > 0 and result is not None:
        try:
            result = send_message(msg)

        except Exception as e:
            print("Probably connection issue:\n", e)
            pass

        time.sleep(5)
        tries -= 1
