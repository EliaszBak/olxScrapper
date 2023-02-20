import csv
import requests
from bs4 import BeautifulSoup

def scrape_olx(name):
    items_list = []

    for page_num in range(1, 100):
        url_with_page = f"https://www.olx.pl/d/elektronika/gry-konsole/gry/q-{name}/?page={page_num}"
        response = requests.get(url_with_page)
        if page_num>1:
            if response.history:
                print(url_with_page)
                print(page_num)
                break
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', {'class': 'offer-wrapper'})

        for item in items:
            title = item.find('a', {'class': 'marginright5'}).text.strip()
            link = item.find('a', {'class': 'marginright5'})['href']
            try:
                price = item.find('p', {'class': 'price'}).text.strip()
                price = int(price.replace(' ', '').replace('zł', ''))
            except:
                price = 'No price'

            items_list.append({'Title': title, 'Price': price, 'Link': link})

    return items_list

def save_to_csv(data, filename):
    with open(filename, mode='w', newline='',  encoding="utf-8") as file:
        fieldnames = ['Title', 'Price', 'Link']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for item in data:
            writer.writerow(item)

name = input("Enter item name: ")
items_list = scrape_olx(name)
save_to_csv(items_list, f"{name}_items.csv")
