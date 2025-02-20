import os
from dotenv import load_dotenv

load_dotenv()

class Environment():
    def __init__(self):
        pass

    def get_deepseek_api_key(self):
        return os.getenv("deepseek-API")
