import requests
from bs4 import BeautifulSoup
import pandas as pd


def Get_Data():
    data = []
    for i in range(1,11):
        URL = 'https://www.sarouty.ma/fr/recherche?c=1&l=35&ob=mr&page='+str(i)
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        Cards = soup.find_all('div', class_="card-list__item")

        #headings =['Prix(x1000 MAD)', 'Description', 'Adresse', 'Surface']

        for Card in Cards:
            data_row = {'Prix(x1000 MAD)': int((Card.find('div', class_="card__price-area").text.replace('MAD', '').replace(',', '').strip())[:-3]),
                        'Description': Card.find('h2', class_="card__title card__title-link").text.replace('\n','').strip(),
                        'Adresse': Card.find('span', class_="card__location-text").text.replace('\n', '').strip(),
                        'Surface': Card.find('p',class_="card__property-amenity card__property-amenity--area").text.replace('\n', '').strip()
                        }
            data.append(data_row)
    return data





def write_csv(Data, file_name):
    df = pd.DataFrame(data=Data)
    df.to_csv(file_name, index=False, mode='w')

def append_csv(Data, file_name):
    df = pd.DataFrame(data=Data)
    df.to_csv(file_name, index=False, header=None, mode='a')

def read_file(file_name):
    df = pd.read_csv(file_name)
    return df


if __name__ == '__main__':
    data = Get_Data()
    write_csv(data, 'out.csv')
    #print(read_file('out.csv'))
