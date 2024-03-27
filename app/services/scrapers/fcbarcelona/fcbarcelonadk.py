from datetime import datetime
from bs4 import BeautifulSoup
import requests
from app.dependencies import get_db_connection
import json
from app.models import article
import re

base_url = "https://fcbarcelona.dk"
article_base_url = "https://fcbarcelona.dk/artikler"

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


def get_articles_from_links(links):
    data = []

    for url in links:
        article_url = base_url + url
        article_data = scrape(article_url)
        parsed_article = parse_article_content(article_data, article_url)
        data.append(parsed_article)

    # Convert data list to JSON format
    ##json_data = json.dumps(data, default=lambda o: o.__dict__, ensure_ascii=False, indent=4)

    return data


def parse_article_content(html, article_url):
    soup = BeautifulSoup(html, "html.parser")
    article_test = soup.find('div', id='article_main')
    print(article_test)

    # Remove unwanted text
    for div in soup.find_all('div', class_='custom'):
        div.decompose()

    for div in soup.find_all('div', class_='yellow'):
        div.decompose()

    # Find the first paragraph element
    article_header = soup.find('div', id='article_header').find('h1').text.strip()

    article_created_at = soup.find('div', id='article_header').find('p').text.strip()
    article_created_at = re.match(r'(.+?)\s*-\s*(.+)', article_created_at).group(2)  # Trim for preceding text

    paragraphs = soup.find_all('p')[1:]

    article_text = [p.get_text(strip=True) for p in paragraphs]
    article_text = ' '.join(article_text)
    article_text = article_text.replace("//", "")

    parsed_article = article.article(title=article_header, content=article_text, created_at=article_created_at,
                                     origin_url=article_url)

    return parsed_article


def get_articles():
    print("Initial scrape. . .")
    html = scrape(base_url + "/artikler")
    print("scraped html, parsing article links. . . ")
    links = get_links(html)
    print("Found links, scraping each article . . .")
    articles = get_articles_from_links(links)
    print("Parsed articles, returning. . .")
    return articles

