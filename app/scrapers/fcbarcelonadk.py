from bs4 import BeautifulSoup
import requests

url = "https://fcbarcelona.dk/Artikler/"


def get_content():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features='html.parser')
    print(soup)


get_content()
