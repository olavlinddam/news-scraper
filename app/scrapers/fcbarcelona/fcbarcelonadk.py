import datetime

from bs4 import BeautifulSoup
import requests
from app.dependencies import get_db_connection
import json
from app.models import article

baseUrl = "https://fcbarcelona.dk"



def scrape(url):
    r = requests.get(url)
    print(r.text)
    return r.text


def get_links(html):
    print("Attempting to get article links. . .")
    soup = BeautifulSoup(html, "html.parser")
    anchor_elements = soup.find_all('a')
    links = []

    for element in anchor_elements:
        href = element.get('href')
        if href and (href.startswith('/Nyheder') or href.startswith('/Video')):
            links.append(href)  # Only append if href starts with the condition

    print(links)
    return links


def get_article_content(links):
    data = []

    for url in links:
        article_url = baseUrl + url
        article_data = scrape(article_url)
        parsed_article = parse_article_content(article_data, article_url)
        data.append(parsed_article)

    # Convert data list to JSON format
    json_data = json.dumps(data, default=lambda o: o.__dict__)

    return json_data



def parse_article_content(html, article_url):
    soup = BeautifulSoup(html, "html.parser")

    # gpt3.5
    # Remove unwanted text
    for div in soup.find_all('div', class_='custom'):
        div.decompose()
    # Find the first paragraph element

    article_header = soup.find('div', id='article_header').find('h1').text.strip()
    try:
        # Check if the content is in the first <p> tag
        article_main = soup.find('div', id='article_main').find_all('p')[1].text.strip()
        if not article_main:
            # If the content is empty, check the second <p> tag
            article_main = soup.find('div', id='article_main').find_all('p')[2].text.strip()
    except IndexError:
        try:
            # If the first attempt fails, try to retrieve the content from the second <p> tag
            article_main = soup.find('div', id='article_main').find_all('p')[2].text.strip()
        except IndexError:
            # If both attempts fail, handle the situation gracefully (e.g., print an error message or assign a default value)
            article_main = "Content not found"

    parsed_article = article.article(title=article_header, content=article_main, created_at=datetime.date,
                                  origin_url=article_url)

    return parsed_article


#get_content()

html1 = scrape(baseUrl + "/artikler")

links = get_links(html1)

get_article_content(links)