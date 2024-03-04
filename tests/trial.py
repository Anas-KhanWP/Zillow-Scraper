import requests
from bs4 import BeautifulSoup

# Specify the index you want to use
index = 1  # You can change this to the desired index

# URL template with index
url = f"https://www.zillow.com/brooklyn-new-york-ny/2_p/?searchQueryState=%7B%22pagination%22%3A%7B%22currentPage%22%3A2%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-74.1131529272461%2C%22east%22%3A-73.72794479736329%2C%22south%22%3A40.56134036879829%2C%22north%22%3A40.78111523910933%7D%2C%22mapZoom%22%3A12%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A37607%2C%22regionType%22%3A17%7D%5D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22con%22%3A%7B%22value%22%3Afalse%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22apa%22%3A%7B%22value%22%3Afalse%7D%2C%22apco%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"

# Send a GET request to the URL without a proxy to get cookies
response_without_proxy = requests.get(url)
print(BeautifulSoup(response_without_proxy.text, 'html.parser'))
cookies = response_without_proxy.cookies

# Specify your proxy information
proxy = {
    'http': 'http://138.68.60.8:8080',
}

# Send a GET request to the URL with the specified proxy and include cookies
response_with_proxy = requests.get(url, proxies=proxy, cookies=cookies)

# Check if the request was successful (status code 200)
if response_with_proxy.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response_with_proxy.text, 'html.parser')

    # Now you can work with the parsed HTML content (soup) as needed
    # For example, print the title of the page
    print("Page Title:", soup.title.text)
else:
    print("Failed to retrieve the page. Status code:", response_with_proxy.status_code)
