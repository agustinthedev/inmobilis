import sqlite3
#from Util import Util

class DB:
    def __init__(self):
        cursor = self.__start_connection()

    def __start_connection(self):
        # TODO: Read db name from config
        # connection = sqlite3.connect(Util().get_db_name())
        connection = sqlite3.connect('inmobilis.db')
        self.connection = connection
        return self.connection.cursor()
    
    def insert_listing(self, listing:dict):
        # TODO: Read query from config, throwing error when importing Util for some reason
        query = "INSERT INTO listings (Title, Link, Raw_Link, Price, Address, Raw_Details, Bedrooms, Bathrooms, Area, Property_Type, Neighborhood, Operation_Type, Scrape_Id) VALUES (%Title%, %Link%, %Raw_Link%, %Price%, %Address%, %Raw_Details%, 0, 0, 0, %Property_Type%, %Neighborhood%, %Operation_Type%, 0)"

        query = query.replace("%Title%", listing['title'])
        query = query.replace("%Link%", listing['link'])
        query = query.replace("%Raw_Link%", listing['raw_link'])
        query = query.replace("%Price%", listing['price'])
        query = query.replace("%Address%", listing['address'])
        query = query.replace("%Raw_Details%", listing['raw_details'])
        query = query.replace("%Property_Type%", listing['property_type'])
        query = query.replace("%Neighborhood%", listing['neighborhood'])
        query = query.replace("%Operation_Type%", listing['operation_type'])

        print(query)