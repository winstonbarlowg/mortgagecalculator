import requests
import re
from bs4 import BeautifulSoup

url = 'https://www.rightmove.co.uk/property-for-sale/property-97702235.html'

headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.16 Safari/537.36'
}

# html_content = requests.get(url).text

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='primaryContent')

price_element = results.find('p', class_='property-header-price')
property_price = price_element.find('strong')
property_location = results.find('address', class_="pad-0 fs-16 grid-25")


print(property_price.text.strip())
print(property_location.text.strip())
