import re
import httpx
import json
import time
from parsel import Selector

def parse_property(data: dict) -> None:
    # print("Data Structure:", data)  # Add this line
    try:
        agent_info = data['props']

        print(agent_info)

    except KeyError as e:
        print(f"Error: Key {e} not found. Please check the structure of the 'data' dictionary.")


if __name__ == "__main__":
    BASE_HEADERS = {
        "accept-language": "en-US,en;q=0.9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-US;en;q=0.9",
        "accept-encoding": "gzip, deflate, br",
    }

    url = "https://www.zillow.com/homedetails/5473-Kings-Hwy-Brooklyn-NY-11203/30656354_zpid/"
    with httpx.Client(http2=True, headers=BASE_HEADERS, follow_redirects=True) as client:
        resp = client.get(url)

    # Add a delay to wait for potential dynamic content loading
    time.sleep(5)  # You may adjust the duration based on your observations

    sel = Selector(text=resp.text)
    print(resp.text)
    script_content = sel.css("script#__NEXT_DATA__::text").get()

    if script_content:
        data = json.loads(script_content)
        # parse_property(data)
    else:
        print("Error: No script content found with the specified CSS selector.")


    # parse_property(data)

    # print(data)
