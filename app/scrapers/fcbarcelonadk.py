from bs4 import BeautifulSoup
import requests
from ..dependencies import get_db_connection

url = "https://fcbarcelona.dk/Artikler/"


def get_content():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features='html.parser')
    print(soup)

def insert_article(article):
    collection = get_db_connection()
    collection.insert_one(article)


get_content()


