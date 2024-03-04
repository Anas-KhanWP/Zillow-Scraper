import os
import time
import datetime
import json
import httpx
import csv
from parsel import Selector


# Function to parse property data and write to CSV
def parse_property(data: dict) -> None:
    try:
        # Extracting list of search results from the data
        list_results = data['props']['pageProps']['searchPageState']['cat1']['searchResults']['listResults']

        # Iterate through each result
        for result in list_results:
            # Extracting relevant information from the result
            broker_name = result.get('brokerName', 'N/A')

            # Handling cases where broker name contains "Listing by:"
            if 'Listing by:' in broker_name:
                broker_name = broker_name.split('Listing by:')[1].strip()

            link_of_listing = result.get('detailUrl', 'N/A')
            address = result.get('address', 'N/A')
            marketing_status = result.get('marketingStatusSimplifiedCd', 'N/A')
            price = result.get('price', 'N/A')
            home_type = result.get('hdpData', {}).get('homeInfo', {}).get('homeType', 'N/A')
            post_at = result.get('variableData', {}).get('text', 'N/A')

            # Writing the extracted data to the CSV file
            csv_writer.writerow(
                [
                    link_of_listing,
                    home_type,
                    city,
                    post_at,
                    address,
                    marketing_status,
                    price,
                    broker_name
                ]
            )

    except KeyError as e:
        # Handling the case where a key is not found in the data dictionary
        print(f"Error: Key {e} not found. Please check the structure of the 'data' dictionary.")


if __name__ == "__main__":
    # Base headers for HTTP requests
    BASE_HEADERS = {
        "accept-language": "en-US,en;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-US;en;q=0.9",
        "accept-encoding": "gzip, deflate, br",
    }

    # URLs for different cities
    city_urls = {
        "Brooklyn": "https://www.zillow.com/brooklyn-new-york-ny/?searchQueryState=%7B%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22north%22%3A40.76278499807343%2C%22south%22%3A40.54712385284077%2C%22east%22%3A-73.73687118896483%2C%22west%22%3A-74.13855881103514%7D%2C%22mapZoom%22%3A12%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22doz%22%3A%7B%22value%22%3A%221%22%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A37607%2C%22regionType%22%3A17%7D%5D%2C%22pagination%22%3A%7B%7D%7D",
        "Queens": "https://www.zillow.com/queens-new-york-ny/?searchQueryState=%7B%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22north%22%3A40.88660150634466%2C%22south%22%3A40.455384810621325%2C%22east%22%3A-73.4297643779297%2C%22west%22%3A-74.23313962207033%7D%2C%22mapZoom%22%3A11%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22doz%22%3A%7B%22value%22%3A%221%22%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A270915%2C%22regionType%22%3A17%7D%5D%2C%22pagination%22%3A%7B%7D%7D",
        "Staten Island": "https://www.zillow.com/staten-island-new-york-ny/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-74.5556346220703%2C%22east%22%3A-73.75225937792968%2C%22south%22%3A40.35614295840351%2C%22north%22%3A40.78799873334689%7D%2C%22mapZoom%22%3A11%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A27252%2C%22regionType%22%3A17%7D%5D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22doz%22%3A%7B%22value%22%3A%221%22%7D%7D%2C%22isListVisible%22%3Atrue%7D",
        "Bronx": "https://www.zillow.com/bronx-new-york-ny/?searchQueryState=%7B%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22north%22%3A40.95778239440057%2C%22south%22%3A40.742753834298405%2C%22east%22%3A-73.64859768896483%2C%22west%22%3A-74.05028531103514%7D%2C%22mapZoom%22%3A12%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22doz%22%3A%7B%22value%22%3A%221%22%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A17182%2C%22regionType%22%3A17%7D%5D%2C%22pagination%22%3A%7B%7D%7D",
        "Manhattan": "https://www.zillow.com/manhattan-new-york-ny/?searchQueryState=%7B%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22north%22%3A40.88831939620082%2C%22south%22%3A40.673065205936155%2C%22east%22%3A-73.77797868896482%2C%22west%22%3A-74.17966631103513%7D%2C%22mapZoom%22%3A12%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22doz%22%3A%7B%22value%22%3A%221%22%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A12530%2C%22regionType%22%3A17%7D%5D%2C%22pagination%22%3A%7B%7D%7D",
        "Nassau County": "https://www.zillow.com/nassau-county-ny/?searchQueryState=%7B%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22north%22%3A41.18444811468382%2C%22south%22%3A40.323101425738066%2C%22east%22%3A-72.79834775585937%2C%22west%22%3A-74.40509824414062%7D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22doz%22%3A%7B%22value%22%3A%221%22%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A1252%2C%22regionType%22%3A4%7D%5D%2C%22pagination%22%3A%7B%7D%7D"
    }

    # Initializing total_results counter
    total_results = 0

    current_date_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Creating a folder with today's date inside "./results" if it doesn't exist
    results_folder = os.path.join("results", datetime.datetime.now().strftime("%Y%m%d"))

    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    result_file = os.path.join(results_folder, f'zillow_results_{current_date_time}.csv')

    # Opening CSV file for writing
    with open(result_file, mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)

        # Writing header row to CSV
        csv_writer.writerow(
            [
                'Link of Listing',
                'Home Type',
                'City',
                'Post At',
                'Address',
                'Status',
                'Price',
                'Broker Name'
            ]
        )

        # Record the start time
        start_time = time.time()

        # Iterating through each city and page index
        for city, url_template in city_urls.items():
            # Constructing search URL
            search_url = url_template.format()

            # Sending HTTP request to the search URL
            with httpx.Client(http2=True, headers=BASE_HEADERS, follow_redirects=True) as client:
                resp = client.get(search_url)

                print(f"resp: {resp}")

            # Parsing the HTML response
            sel = Selector(text=resp.text)
            print(f"html: {sel}")
            script_content = sel.css("script#__NEXT_DATA__::text").get()

            # Checking if script content is present in the HTML
            if script_content:
                data = json.loads(script_content)
                # print(f"Data found for {city} - Page {index}:")

                # Calling the parse_property function to extract and write data to CSV
                parse_property(data)

                # Incrementing total_results with the number of results found on this page
                total_results += len(
                    data['props']['pageProps']['searchPageState']['cat1']['searchResults']['listResults'])

                # print(f"Total results so far: {total_results}")
                # print(f"Current Page Number: {index}")
            else:
                print(f"No script content found")
                continue

        # Record the end time
        end_time = time.time()

        # Calculate the total duration in seconds
        total_duration = end_time - start_time

        # Format the total duration as "hh:mm:ss"
        hours, remainder = divmod(total_duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted_duration = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

        print(f"Total time taken: {formatted_duration}")

    print("Total Results:", total_results)
