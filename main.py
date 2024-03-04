import requests
from bs4 import BeautifulSoup
import time

header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
          'referer':'https://www.zillow.com/homes/Missoula,-MT_rb/'}

data = requests.get('https://www.zillow.com/homedetails/5473-Kings-Hwy-Brooklyn-NY-11203/30656354_zpid/', headers=header)

# time.sleep(5)

soup = BeautifulSoup(data.text, "lxml")

print(soup)

listing_by = soup.find_all('p', {'class':'Text-c11n-8-84-3__sc-aiai24-0 hrfydd'})
# price = soup.find_all('span', {'data-test':'property-card-price'})
# seller = soup.find_all('div', {'class':'cWiizR'})

print(listing_by)
# print(price)
# print(seller)

# adr=[]
# pr=[]
# sl=[]
#
# for result in address:
#     adr.append(result.text)
# for result in price:
#     pr.append(result.text)
# for result in seller:
#     sl.append(result.text)
# print(adr)
# print(pr)
# print(sl)

# div = soup.find("div", {'id' : 'grid-search-results'})
#
# ul = div.find('ul',{'class':'List-c11n-8-84-3__sc-1smrmqp-0 StyledSearchListWrapper-srp__sc-1ieen0c-0 doa-doM fgiidE photo-cards photo-cards_extra-attribution'})
#
# # Find all li elements within the ul element
# li_elements = ul.find_all('li', {'class': 'ListItem-c11n-8-84-3__sc-10e22w8-0 StyledListCardWrapper-srp__sc-wtsrtn-0 iCyebE gTOWtl'})
#
# print(li_elements)
#
# i = 0
# # Print the text content of each li element
# for li in li_elements:
#     property_link = li.find('a', {'class': 'StyledPropertyCardDataArea-c11n-8-84-3__sc-yipmu-0 jnnxAW property-card-link'})
#     href_value = property_link.get('href')
#     print(href_value)
#     i += 1
#     print(i)

# for address in addresses:
#     # Find the <a> tags within each address with data-test="property-card-link"
#     property_links = address.find_all('a', {'class': 'StyledPropertyCardDataArea-c11n-8-84-3__sc-yipmu-0 jnnxAW property-card-link'})
#
#     # Print the href values of the property links
#     for link in property_links:
#         href_value = link.get('href')
#         print(href_value)

