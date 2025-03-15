import sqlite3, os.path
from datetime import datetime
#from Util import Util

class DB:
    def __init__(self):
        self.connection = self.__start_connection()
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def __start_connection(self):
        # TODO: Read db name from config
        # connection = sqlite3.connect(Util().get_db_name())
        connection = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), "inmobilis.db"))
        return connection

    def create_new_scrape_id(self):
        query = "INSERT INTO scrape_ids(Date) VALUES (?)"
        insert_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        exec = self.connection.cursor().execute(query, (insert_date,))
        self.connection.commit()
        scrape_id = exec.lastrowid

        return str(scrape_id)
    
    def get_roi_alert_number(self):
        query = "SELECT roi_alert FROM settings"
        exec = self.connection.cursor().execute(query)
        return exec.fetchone()
    
    def get_price_alert_number(self):
        query = "SELECT price_alert FROM settings"
        exec = self.connection.cursor().execute(query)
        return exec.fetchone()
    
    def get_urls_to_scrape(self):
        query = "SELECT Url, Neighborhood FROM scrape_urls WHERE Enabled = '1'"
        exec = self.connection.cursor().execute(query)
        return exec.fetchall()
    
    def get_neighborhoods_with_interest(self):
        query = "SELECT DISTINCT Neighborhood FROM scrape_urls WHERE Interest = '1'"
        exec = self.connection.cursor().execute(query)
        return exec.fetchall()
    
    def get_scrape_results_listings(self, scrape_id:str, operation_type:str):
        query = f"SELECT * FROM listings WHERE Scrape_Id='{scrape_id}' AND Operation_Type='{operation_type}'"
        exec = self.connection.cursor().execute(query)
        return exec.fetchall()

    def get_median_price(self, scrape_id:str, operation:str, neighborhood:str, bedrooms:str, exclude_types:str):
        query = f'SELECT MAX(Price) AS "Median" FROM (SELECT Price, NTILE(4) OVER(ORDER BY Price) AS Quartile FROM listings WHERE Scrape_Id = "{scrape_id}" AND Operation_Type = "{operation}" AND Bedrooms = "{bedrooms}" AND Neighborhood = "{neighborhood}" AND Property_Type NOT IN ("{exclude_types}")) X WHERE Quartile = 2'
        exec = self.connection.cursor().execute(query)
        return int(exec.fetchone()[0])
    
    def listing_with_url_exists(self, url):
        # TODO: Check if listing is in (current_scrape_id - 1) before returning
        query = "SELECT * FROM listings WHERE Link = ?"
        exec = self.connection.cursor().execute(query, (url,))
        results = exec.fetchall()
        return True if results else False
        

    def insert_listing(self, listing:dict):
        # TODO: Read query from config, throwing error when importing Util for some reason
        # query = "INSERT INTO listings (Title, Link, Raw_Link, Price, Address, Raw_Details, Bedrooms, Bathrooms, Area, Property_Type, Neighborhood, Operation_Type, Scrape_Id) VALUES (%Title%, %Link%, %Raw_Link%, %Price%, %Address%, %Raw_Details%, 0, 0, 0, %Property_Type%, %Neighborhood%, %Operation_Type%, 0)"
        query = "INSERT INTO listings (Title, Link, Raw_Link, Price, Address, Raw_Details, Bedrooms, Bathrooms, Area, Property_Type, Neighborhood, Operation_Type, Scrape_Id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        print(query)

        self.connection.cursor().execute(query, (listing['title'], listing['link'], listing['raw_link'], listing['price'], listing['address'], listing['raw_details'], listing['bedrooms'], listing['bathrooms'], listing['area'], listing['property_type'], listing['neighborhood'], listing['operation_type'], listing['scrape_id']))
        self.connection.commit()