import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import csv

user = UserAgent

HEADERS = {
    'User-Agent': user,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
}

def writing(pages, names_list, urls_list, address_list):

    # sources (url, requests, Beautifulsoup)
    iterations = 1
    last_page = False

    # cycle
    while not last_page:
        URL = f"https://www.yellowpages.pl/listing/adres/?ctr=PL&p={pages}"
        req = requests.get(URL).text
        soup = BeautifulSoup(req, 'lxml')

        # cards with content
        cards = soup.find_all('div', class_='cc-content')

        # another content (name, card url, address)

        # names scraping
        try:
            names = soup.find_all('h2', class_='card__title')
        except Exception:
            print(f'[ERROR] - Не знайдено даних про адресу')

        for name in names:
            name = name.text
            names_list.append(name.strip())

        # url scraping
        try:
            urls = soup.find_all('h2', class_='card__title')
        except Exception:
            print(f'[ERROR] - Не знайдено даних про url')

        for url in urls:
            result_url = url.find_all('a')

            for u in result_url:
                result_url = u['href']
                urls_list.append(result_url)

        # address scraping
        try:
            addresses = soup.find_all('address', itemprop='address')
        except Exception:
            print(f'[ERROR] - Не знайдено даних про адресу')

        for address in addresses:
            address = address.get_text(strip=True)
            address_list.append(address)
            print(iterations)
            iterations += 1

        if not cards:
            last_page = True

        pages += 1

    try:
        with open('yellow_pages.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            for name_writing, url_writing, address_writing in zip(names_list, urls_list, address_list):
                writer.writerow([name_writing, url_writing, address_writing])
    except Exception as e:
        print(F'Не можемо відкрити файл. [ERROR]: {e}')

    print(f'Дані успішно записані у csv: {file}')






def main():
    writing(1, [], [], [])

if __name__ == '__main__':
    main()