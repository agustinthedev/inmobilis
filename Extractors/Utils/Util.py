import os, json
from dotenv import load_dotenv

load_dotenv()

class Util():
    def __init__(self):
        self.config = self.get_config()

    def get_config(self):
        return json.load(open(os.getenv("config_file_path")))
    
    def get_db_name(self):
        return self.config["database"]["name"]
    
    def get_insert_listing_query(self):
        return self.config["database"]["insert_listing_query"]

    def get_deepseek_api_key(self):
        return os.getenv("deepseek-API")
    
    def get_telegram_bot_token(self):
        return os.getenv("telegram_bot_token")
    
    def get_telegram_chat_id(self):
        return os.getenv("telegram_chat_id")
