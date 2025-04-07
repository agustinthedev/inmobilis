import sqlite3, os.path
from datetime import datetime
#from Util import Util

class DB:
    def __init__(self):
        self.connection = self.start_connection()
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    def start_connection(self):
        # TODO: Read db name from config
        connection = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), "inmobilis.db"))
        return connection

    def create_new_scrape_id(self):
        self.connection = self.start_connection()
        query = "INSERT INTO scrape_ids(Date) VALUES (?)"
        insert_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        exec = self.connection.cursor().execute(query, (insert_date,))
        self.connection.commit()
        scrape_id = exec.lastrowid

        self.connection.close()

        return str(scrape_id)
    
    def get_roi_alert_number(self):
        self.connection = self.start_connection()
        query = "SELECT roi_alert FROM settings"
        exec = self.connection.cursor().execute(query)
        roi_alert_number = float(exec.fetchone()[0])

        self.connection.close()
        return roi_alert_number
    
    def get_price_alert_number(self):
        self.connection = self.start_connection()
        query = "SELECT price_alert FROM settings"
        exec = self.connection.cursor().execute(query)
        price_alert_number = float(exec.fetchone()[0])

        self.connection.close()
        return price_alert_number
    
    def get_urls_to_scrape(self):
        self.connection = self.start_connection()
        query = "SELECT Url, Neighborhood FROM scrape_urls WHERE Enabled = '1'"
        exec = self.connection.cursor().execute(query)
        urls_to_scrape = exec.fetchall()

        self.connection.close()
        return urls_to_scrape
    
    def get_neighborhoods_with_interest(self):
        self.connection = self.start_connection()
        query = "SELECT DISTINCT Neighborhood FROM scrape_urls WHERE Interest = '1'"
        exec = self.connection.cursor().execute(query)
        neighborhoods_with_interest = exec.fetchall()

        self.connection.close()
        return neighborhoods_with_interest
    
    def get_scrape_results_listings(self, scrape_id:str, operation_type:str):
        self.connection = self.start_connection()
        query = f"SELECT * FROM listings WHERE Scrape_Id='{scrape_id}' AND Operation_Type='{operation_type}'"
        exec = self.connection.cursor().execute(query)
        scrape_results_listings = exec.fetchall()

        self.connection.close()
        return scrape_results_listings
    
    def get_listing_by_row_id(self, row_id:str, operation_type:str):
        self.connection = self.start_connection()
        query = f"SELECT * FROM listings WHERE Id='{row_id}' AND Operation_Type='{operation_type}'"
        exec = self.connection.cursor().execute(query)
        listing = exec.fetchall()

        self.connection.close()
        return listing

    def get_median_price(self, scrape_id:str, operation:str, neighborhood:str, bedrooms:str, exclude_types:str):
        self.connection = self.start_connection()
        query = f'SELECT MAX(Price) AS "Median" FROM (SELECT Price, NTILE(4) OVER(ORDER BY Price) AS Quartile FROM listings WHERE Scrape_Id = "{scrape_id}" AND Operation_Type = "{operation}" AND Bedrooms = "{bedrooms}" AND Neighborhood = "{neighborhood}" AND Property_Type NOT IN ("{exclude_types}")) X WHERE Quartile = 2'
        exec = self.connection.cursor().execute(query)
        median_price = exec.fetchone()[0]

        self.connection.close()
        return median_price
    
    def listing_with_url_exists(self, url):
        self.connection = self.start_connection()
        # TODO: Check if listing is in (current_scrape_id - 1) before returning
        query = "SELECT * FROM listings WHERE Link = ?"
        exec = self.connection.cursor().execute(query, (url,))
        results = exec.fetchall()

        self.connection.close()
        return True if results else False
        

    def insert_listing(self, listing:dict):
        self.connection = self.start_connection()
        # TODO: Read query from config, throwing error when importing Util for some reason
        query = "INSERT INTO listings (Title, Link, Raw_Link, Price, Address, Raw_Details, Bedrooms, Bathrooms, Area, Property_Type, Neighborhood, Operation_Type, Scrape_Id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        exec = self.connection.cursor().execute(query, (listing['title'], listing['link'], listing['raw_link'], listing['price'], listing['address'], listing['raw_details'], listing['bedrooms'], listing['bathrooms'], listing['area'], listing['property_type'], listing['neighborhood'], listing['operation_type'], listing['scrape_id']))
        self.connection.commit()
        listing_id = exec.lastrowid

        self.connection.close()
        return listing_id

    def insert_opportunity_sent(self, url:str):
        self.connection = self.start_connection()
        insert_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        query = "INSERT INTO sent_opportunities(Url, Timestamp) VALUES(?, ?)"

        self.connection.cursor().execute(query, (url, insert_date))
        self.connection.commit()

        self.connection.close()

    def opportunity_sent_exists(self, url:str):
        self.connection = self.start_connection()
        query = f"SELECT Id FROM sent_opportunities WHERE Url=?"
        exec = self.connection.cursor().execute(query, (url,))
        results = exec.fetchall()

        self.connection.close()
        return True if results else False