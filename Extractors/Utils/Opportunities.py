from .DB import DB
from .Telegram import Telegram
from .Util import Util

class Opportunities:
    def __init__(self, scrape_id, listings):
        self.scrape_id = scrape_id
        self.listings_to_process = listings
        self.db = DB()
        self.telegram = Telegram()

    def __send_notification(self, url:str, text:str):
        if not DB().opportunity_sent_exists(url=url):
            DB().insert_opportunity_sent(url=url)
            self.telegram.send_alert(text=text)

    def process_results(self):
        for individual_listing in self.listings_to_process:
            listings = self.db.get_listing_by_row_id(row_id=str(individual_listing), operation_type="Venta")

            for listing in listings:
                price = int(listing[4])
                median_rent = self.db.get_median_price(
                    scrape_id=self.scrape_id, # TODO: maybe use scrape_id - 1? now first runs will have partial data to determine ROI. If implemented, first run needs to be without Opportunities module.
                    operation="Alquiler",
                    neighborhood=str(listing[11]),
                    bedrooms=str(listing[7]),
                    exclude_types="Residencia"
                )
                roi_alert = self.db.get_roi_alert_number()
                price_alert = self.db.get_price_alert_number()
                dolar_price = Util().get_dolar_price()

                calculated_roi = (((median_rent/dolar_price)*12)*100)/price if median_rent else None
                print(f"[!] {str(individual_listing)} - Calculated ROI: {str(calculated_roi)} || Price: {str(price)}")

                if median_rent and calculated_roi >= roi_alert:
                    #TODO: Send Telegram message
                    notification_text = f"[!] ROI Alert\n\nCalculated ROI: {str(calculated_roi)}\nPrice: {str(price)}\nLink: {listing[2]}"
                    self.__send_notification(url=listing[2], text=notification_text)

                elif price <= price_alert:
                    notification_text = f"[!] Price Alert\n\nPrice: {str(price)}\nLink: {listing[2]}"
                    self.__send_notification(url=listing[2], text=notification_text)