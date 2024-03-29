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
    return r.text


def get_links(html):
    print("Extracting links from html. . .")
    soup = BeautifulSoup(html, "html.parser")
    anchor_elements = soup.find_all('a')
    links = []

    for element in anchor_elements:
        href = element.get('href')
        if href and (href.startswith('/Nyheder') or href.startswith('/Video')):
            links.append(href)

    return list(dict.fromkeys(links))


def get_content_from_articles(links):
    data = []

    for url in links:
        article_url = base_url + url
        article_data = scrape(article_url)
        parsed_article = parse_article_content(article_data, article_url)
        data.append(parsed_article)

    return data


def parse_article_content(html, article_url):
    """
    Parse the content of an article from HTML.

    Args:
        html (str): The HTML content of the article.
        article_url (str): The URL of the article.

    Returns:
        article.article: An instance of the article class with parsed content.
    """

    soup = BeautifulSoup(html, "html.parser")

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


def scrape_and_parse_articles():
    print("Attempting to get articles")
    html = scrape(base_url + "/artikler")
    print("Scraped html. ")
    links = get_links(html)
    print("Found links")
    articles = get_content_from_articles(links)
    print("Parsed articles, returning. . .")
    return articles



