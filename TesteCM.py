import requests
from bs4 import BeautifulSoup
from csv import DictWriter
from time import sleep

base_url = 'http://quotes.toscrape.com/'
url = '/page/1'
quote_list = []

while url:
    response = requests.get(f'{base_url}{url}')
    print(f'Now scraping {base_url}{url}')
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find_all(class_='quote')

    
    for quote in quotes:
        quote_list.append({
            'text': quote.find(class_='text').get_text(),
            'author': quote.find(class_='author').get_text(),
            'bio-link': quote.find('a')['href']
        })

  
    next_btn = soup.find(class_='next')
    url = next_btn.find('a')['href'] if next_btn else None
    
   

def write_quotes(quotes):
    with open('quotes.csv', 'w') as file:
        headers = ['text', 'author', 'bio-link']
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()
        for quote in quotes:
            csv_writer.writerow(quote)

write_quotes(quote_list)
