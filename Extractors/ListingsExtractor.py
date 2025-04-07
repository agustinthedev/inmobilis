import requests, argparse, sys
from lxml.html import fromstring
from Utils.DB import DB
from Utils.Util import Util
from Utils.Opportunities import Opportunities

#https://listado.mercadolibre.com.uy/inmuebles/venta/montevideo/_ITEM*CONDITION_2230284_NoIndex_True - NUEVO
#https://listado.mercadolibre.com.uy/inmuebles/venta/montevideo/_ITEM*CONDITION_2230581_NoIndex_True - USADO

# TODO: Define list of all types of properties wanted for scrape (apartamentos, casa, cochera, etc) and get URLs
# TODO: Define list of all neighborhoods and get slugs
# TODO: Create process to get all URLs needed for scrape by mixing types of properties and neighborhoods
# TODO: Check currency type and convert before inserting

#url = 'https://listado.mercadolibre.com.uy/inmuebles/apartamentos/alquiler/montevideo/aguada/_Desde_%index%_NoIndex_True'
results = []
database = DB()
util = Util()

def extract_value(soup, locator, index):
    try:
        return soup.xpath(locator)[index].text_content()
    except Exception:
        return "Unknown"
    
# TODO: Move to Util file
def get_operation_type(url):
    if "/venta/" in str(url).lower():
        return "Venta"
    
    if "/alquiler/" in str(url).lower():
        return "Alquiler"
    
    return "Unknown"
        
# TODO: Move to Util file
def get_property_type(url, title):
    if "residencia" in str(title).lower():
        return "Residencia"

    if "/apartamentos/" in str(url).lower():
        return "Apartamento"
    
    if "/casas/" in str(url).lower():
        return "Casa"
    
    return "Unknown"

def start_scraping(url, neighborhood, scrape_id):
    index = 1

    while True:
        request_url = url.replace("%index%", str(index))
        print(f"[!] Sending request to: {request_url}")
        response = requests.get(request_url)

        index += 48

        soup = fromstring(response.text)

        main_selector = "//div[@class='poly-card__content']"
        listings = soup.xpath(main_selector)

        print(f"[!] Listings detected: {str(len(listings))}.")

        if len(listings) > 0:
            print("[!] Starting scrapping.")
            for i in range(0, len(listings)):
                print(f"Iteration: {str(i)}")
                title_selector = f"//h3[@class='poly-component__title-wrapper']"
                link_selector = f"{title_selector}//a"
                price_selector = f"//span[@class='andes-money-amount__fraction']"
                location_selector = f"//span[@class='poly-component__location']"
                details_delector = f"//div[@class='poly-component__attributes-list']"

                title = soup.xpath(title_selector)[i].text_content()
                link = soup.xpath(link_selector)[i].get('href')
                price = str(soup.xpath(price_selector)[i].text_content()).replace(".", "")
                location = soup.xpath(location_selector)[i].text_content()
                details =  extract_value(soup, details_delector, i) #TODO: Create alert for these cases
                print(f"Title: {title} // Price: {str(price)} // Details: {details} // Location: {location} // Link: {link} \n\n")

                parsed_details = util.format_details(details, title)

                result = {
                    "title": title,
                    "link": str(link).split("#")[0],
                    "raw_link": link,
                    "price": price,
                    "address": location,
                    "raw_details": details,
                    "bedrooms": parsed_details['bedrooms'],
                    "bathrooms": parsed_details['bathrooms'],
                    "area": parsed_details['area'],
                    "property_type": get_property_type(url, title),
                    "neighborhood": neighborhood,
                    "operation_type": get_operation_type(url),
                    "scrape_id": str(scrape_id)
                }

                database.insert_listing(result)

                results.append(result)
        else:
            print("[!] No more listing available. Stopping scrapping.")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument("--url")
    parser.add_argument("--neighborhood")
    parser.add_argument("--scrapeid")

    args = parser.parse_args(sys.argv[1:])

    start_scraping(url=args.url, neighborhood=args.neighborhood, scrape_id=args.scrapeid)

    print(f"[!] Final count of results: {str(len(results))}.")
    #TODO: Implement final results amoutn checker to detect big changes in amount of records scraped.

    Opportunities(scrape_id=str(str(args.scrapeid))).process_results()