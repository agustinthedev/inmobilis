from telebot_router import TeleBot
from .Util import Util

class Telegram:
    def __init__(self):
        self.app = TeleBot(__name__)
        self.app.config['api_key'] = Util().get_telegram_bot_token()
        self.chat_id = Util().get_telegram_chat_id()

    def send_alert(self, text:str):
        self.app.send_message(chat_id=self.chat_id, text=text)