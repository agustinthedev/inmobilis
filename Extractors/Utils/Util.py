import os, json, re, requests
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
    
    def get_dolar_price(self):
        req = requests.get(self.get_config()['endpoints']['dolar-price'])
        return req.json()['venta']
    
    def format_details(self, raw_details:str, title:str):
        details = {}
        
        bedrooms = re.findall("(\d+)\s+(?=dormitorio)", raw_details)
        details['bedrooms'] = str(bedrooms[0]) if len(bedrooms) > 0 else "0"

        bathrooms = re.findall("(\d+)\s+(?=baño)", raw_details)
        details['bathrooms'] = str(bathrooms[0]) if len(bathrooms) > 0 else "0"

        area = re.findall("(\d+)\s+(?=m² cubiertos)", raw_details)
        details['area'] = str(area[0]) if len(area) > 0 else "0"

        if "monoambiente" in title.lower() or "mono ambiente" in title.lower():
            print(f"[!] Monoambiente detected, changing bedrooms amount to 0.")
            details['bedrooms'] = "0"

        return details

