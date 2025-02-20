import requests
from lxml.html import fromstring
from Utils.DB import DB

# TODO: Define list of all types of properties wanted for scrape (apartamentos, casa, cochera, etc) and get URLs
# TODO: Define list of all neighborhoods and get slugs
# TODO: Create process to get all URLs needed for scrape by mixing types of properties and neighborhoods

url = 'https://listado.mercadolibre.com.uy/inmuebles/apartamentos/alquiler/montevideo/aguada/_Desde_%index%_NoIndex_True'
index = 1
results = []
database = DB()

def extract_value(soup, locator, index):
    try:
        return soup.xpath(locator)[index].text_content()
    except Exception:
        return "Unknown"

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

            result = {
                "title": title,
                "link": str(link).split("#")[0],
                "raw_link": link,
                "price": price,
                "address": location,
                "raw_details": details,
                "property_type": "Casa", # TODO: remove hardcode
                "neighborhood": "Aguada", # TODO: remove hardcode
                "operation_type": "Alquiler" # TODO: remove hardcode
            }

            database.insert_listing(result)

            results.append(result)
    else:
        print("[!] No more listing available. Stopping scrapping.")
        break

print(f"[!] Final count of results: {str(len(results))}.")