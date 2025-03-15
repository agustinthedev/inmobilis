from .DB import DB
from .Telegram import Telegram
from .Util import Util

class Opportunities:
    def __init__(self, scrape_id):
        self.scrape_id = scrape_id
        self.db = DB()

    def process_results(self):
        listings = self.db.get_scrape_results_listings(scrape_id=self.scrape_id, operation_type="Venta")

        for listing in listings:
            price = int(listing[4])
            median_rent = self.db.get_median_price(
                scrape_id=self.scrape_id,
                operation="Alquiler",
                neighborhood=str(listing[11]),
                bedrooms=str(listing[7]),
                exclude_types="Residencia"
            )
            roi_alert = self.db.get_roi_alert_number()
            price_alert = self.db.get_price_alert_number()
            dolar_price = Util().get_dolar_price()

        if ((median_rent/dolar_price)*100)/price >= roi_alert or price <= price_alert:
            if not DB().opportunity_sent_exists(url=listing[2]):
                print("[!] Opportunity detected.")
                DB().insert_opportunity_sent(url=listing[2])

                #TODO: Send Telegram message