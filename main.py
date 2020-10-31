"""This code scrap the data of 10 pages in www.sarouty.ma.
the data is fetched into out.csv file
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd


def write_csv(data_: list, file_name: str):
    """A function to write the data fetched to a csv file"""
    df = pd.DataFrame(data=data_)
    df.to_csv(file_name, index=False, mode='w')


def read_file(file_name: str):
    """A function to read a csv file"""
    df = pd.read_csv(file_name)
    return df


def scrap_page(url: str) -> list:
    """A function to scrap the page url in parameter and set it as a valid data to store in csv file"""
    page_data = []
    page = requests.get(url)
    page_soup = BeautifulSoup(page.content, 'html.parser')
    # The wanted informations are layed in list of cards in the pages
    cards = page_soup.find_all('div', class_="card-list__item")
    # Iterating Through cards
    for card in cards:
        data_row = {'Prix(x1000 MAD)': format_price(format_string(card, 'div', 'card__price-area')),
                    'Description': format_string(card, 'h2', 'card__title card__title-link'),
                    'Adresse': format_string(card, 'span', "card__location-text"),
                    'Surface': format_string(card, 'p', "card__property-amenity card__property-amenity--area")
                    }
        page_data.append(data_row)
    return page_data


def format_string(card: list, tag: str, class_: str) -> str:
    """A function to strip the fetched string data by removing Leading and trailing whitespaces and line break"""
    return card.find(tag, class_=class_).text.replace('\n', '').strip()


def format_price(raw_price: str) -> float:
    """A function to format string price to float Price"""
    return float(raw_price.replace('MAD', '').replace(',', '')) * 0.001


if __name__ == '__main__':
    data = []
    NBR_PAGES = 10
    # Iterating Through pages
    for page in range(1, NBR_PAGES + 1):
        url = 'https://www.sarouty.ma/fr/recherche?c=1&l=35&ob=mr&page=' + str(page)
        data.append(scrap_page(url))
    write_csv(data, 'out.csv')
