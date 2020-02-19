import requests
import re
from bs4 import BeautifulSoup

url = 'https://www.hsbc.co.uk/mortgages/our-rates/'

headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.16 Safari/537.36'
}

# html_content = requests.get(url).text

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

# fixed rate mortgages 
ltv_95 = soup.find(id='content_main_basicTable_1')
ltv_90 = soup.find(id='content_main_basicTable_2')
ltv_85 = soup.find(id='content_main_basicTable_3')
ltv_80 = soup.find(id='content_main_basicTable_4')

rates = []
for p in ltv_95.find_all('p'):
    bold = p.find_all('strong')
    rates.append(bold)
    # print(bold)
    # rate = p.find_all(string='fixed')
    # print(rate)

print(rates[0])

