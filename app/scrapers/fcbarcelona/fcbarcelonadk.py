import datetime

from bs4 import BeautifulSoup
import requests
from app.dependencies import get_db_connection
import json
from app.models import article

base_url = "https://fcbarcelona.dk"


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
        article_url = base_url + url
        article_data = scrape(article_url)
        parsed_article = parse_article_content(article_data, article_url)
        data.append(parsed_article)

    # Convert data list to JSON format
    json_data = json.dumps(data, default=lambda o: o.__dict__)

    return json_data


def parse_article_content(html, article_url):
    soup = BeautifulSoup(html, "html.parser")
    article_test = soup.find('div', id='article_main')
    print(article_test)

    # gpt3.5
    # Remove unwanted text
    for div in soup.find_all('div', class_='custom'):
        div.decompose()

    for div in soup.find_all('div', class_='yellow'):
        div.decompose()


    # Find the first paragraph element
    article_header = soup.find('div', id='article_header').find('h1').text.strip()
    paragraphs = soup.find_all('p')[1:]
    article_text = [p.get_text(strip=True) for p in paragraphs]

    # Join the extracted text into a single string
    article_text = ' '.join(article_text)
    article_text = article_text.replace("//", "")

    parsed_article = article.article(title=article_header, content=article_text, created_at=datetime.datetime.now(),
                                     origin_url=article_url)

    return parsed_article


def test():
    html = scrape(base_url + "/artikler")
    links = get_links(html)
    json_dump = get_article_content(links)
    print(json_dump)



test()