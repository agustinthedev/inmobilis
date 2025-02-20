import os, json
from dotenv import load_dotenv

load_dotenv()

class Util():
    def __init__(self):
        pass

    def get_config(self):
        return json.load(open("config.json"))

    def get_deepseek_api_key(self):
        return os.getenv("deepseek-API")
