import os
import time
import random
import json
import httpx
import pandas as pd
from scrapy import Selector
from datetime import datetime, timedelta


class ZillowScraper:
    """
    The ZillowScraper class contains methods for scraping real estate data from Zillow.com.

    Args:
        None

    Returns:
        A pandas DataFrame containing the scraped data.

    Raises:
        ValueError: If the input data is not in the expected format.
    """

    def __init__(self):
        # Initialize a list of RapidAPI keys for rotating usage
        self.rapidapi_keys = [
            "d376ac8d6amsh71c43b1ae6e6e76p106aaajsn9564fb4e9d93",
            "6290c2073amsh3c8ccdb2a0e82dep17d44djsn277c3f25996c",
            "714491bb85mshbc5f3701c723d68p1317e9jsnf79606287a32",
            "1814c34213mshe76bd4a2100cdf2p1be9d2jsn8181b6f78fcd",
            "77196c2c37mshb126bee22941426p1e3c13jsn890467e71ed0",
            "7194c276cdmsh58c082395680bd2p14de12jsn76227b39c61a"
        ]

    def rotate_rapidapi_key(self):
        """Rotate RapidAPI key for each API request."""
        return random.choice(self.rapidapi_keys)

    def convert_time_interval(self, interval):
        """
        Convert time intervals like '2 hours ago' to a datetime format.

        Args:
            interval (str): Time interval string.

        Returns:
            str: Formatted time string.

        """
        current_time = datetime.now()

        if "minutes ago" in interval:
            minutes_ago = int(interval.split()[0])
            post_time = current_time - timedelta(minutes=minutes_ago)
        elif "hour ago" in interval or "hours ago" in interval:
            hours_ago = int(interval.split()[0])
            post_time = current_time - timedelta(hours=hours_ago)
        else:
            # Handle other cases or return 'N/A' if the format is not recognized
            return interval

        # Format the result as "Jan 15 at 2pm"
        formatted_time = post_time.strftime("%b %d at %I%p")

        return formatted_time

    def parse_property(self, data: dict, city) -> pd.DataFrame:
        """
        Parse the JSON data returned from the API and extract relevant property information.

        Args:
            data (dict): JSON data returned from the API.
            city (str): Name of the city.

        Returns:
            pd.DataFrame: DataFrame containing parsed property information.

        """
        results_list = []
        try:
            # Extracting list of search results from the data
            list_results = data["props"]["pageProps"]["searchPageState"]["cat1"]["searchResults"]["listResults"]

            # Iterate through each result
            for result in list_results:
                # Extracting relevant information from the result
                broker_name = result.get("brokerName", "N/A")

                # Handling cases where broker name contains "Listing by:"
                if "Listing by:" in broker_name:
                    broker_name = broker_name.split("Listing by:")[1].strip()

                link_of_listing = result.get("detailUrl", "N/A")
                address = result.get("address", "N/A")
                marketing_status = result.get("marketingStatusSimplifiedCd", "N/A")
                price = result.get("price", "N/A")
                home_type = result.get("hdpData", {}).get("homeInfo", {}).get("homeType", "N/A")
                post_at = result.get("variableData", {}).get("text", "N/A")
                post_at = self.convert_time_interval(post_at)

                # Writing the extracted data to the DataFrame
                results_list.append([
                    link_of_listing,
                    home_type,
                    city,
                    post_at,
                    address,
                    marketing_status,
                    price,
                    broker_name,
                ])

        except KeyError as e:
            # Handling the case where a key is not found in the data dictionary
            print(f"Error: Key {e} not found. Please check the structure of the 'data' dictionary.")

        return pd.DataFrame(
            results_list,
            columns=[
                "Link of Listing",
                "Home Type",
                "City",
                "Post At",
                "Address",
                "Status",
                "Price",
                "Broker Name",
            ],
        )

    def scrape_results(self):
        """
        Scrape real estate data from Zillow for multiple cities.

        Returns:
            pd.DataFrame: DataFrame containing scraped property data.

        """
        BASE_HEADERS = {
            "X-RapidAPI-Key": self.rotate_rapidapi_key(),
            "X-RapidAPI-Host": "getproxylist-getproxylist-v1.p.rapidapi.com",
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
            "Nassau County": "https://www.zillow.com/nassau-county-ny/?searchQueryState=%7B%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22north%22%3A41.18444811468382%2C%22south%22%3A40.323101425738066%2C%22east%22%3A-72.79834775585937%2C%22west%22%3A-74.40509824414062%7D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%2C%22doz%22%3A%7B%22value%22%3A%221%22%7D%7D%2C%22isListVisible%22%3Atrue%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A1252%2C%22regionType%22%3A4%7D%5D%2C%22pagination%22%3A%7B%7D%7D",
        }

        total_results = 0
        results_list = []

        current_date_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_folder = os.path.join("results", datetime.now().strftime("%Y%m%d"))

        if not os.path.exists(results_folder):
            os.makedirs(results_folder)

        start_time = time.time()

        for city, url_template in city_urls.items():
            search_url = url_template.format()
            print(search_url)
            with httpx.Client(
                    http2=True, headers=BASE_HEADERS, follow_redirects=True
            ) as client:
                resp = client.get(search_url)

            sel = Selector(text=resp.text)
            script_content = sel.css("script#__NEXT_DATA__::text").get()

            if script_content:
                data = json.loads(script_content)
                df = self.parse_property(data, city)
                results_list.append(df)

                total_results += len(
                    data["props"]["pageProps"]["searchPageState"]["cat1"]["searchResults"][
                        "listResults"
                    ]
                )

        end_time = time.time()
        total_duration = end_time - start_time
        hours, remainder = divmod(total_duration, 3600)
        minutes, seconds = divmod(remainder, 60)

        print(f"Scraping completed in {int(hours)} hours, {int(minutes)} minutes and {int(seconds)} seconds.")
        print(f"Total number of results: {total_results}")

        # Concatenate all DataFrames into one
        full_df = pd.concat(results_list, ignore_index=True)

        # Save the DataFrame to a CSV file
        full_df.to_csv(
            os.path.join(results_folder, f"zillow_results_{current_date_time}.csv"), index=False
        )

        return full_df


# Instantiate the scraper object
scraper = ZillowScraper()

# Scrape Zillow data
zillow_data = scraper.scrape_results()
