import queue
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from app.dependencies import get_db_connection
import json
from app.models import news_article
import re

base_url = "https://fcbarcelona.dk"
article_base_url = "https://fcbarcelona.dk/artikler"
fcb_news_queue = queue.Queue(maxsize=15)
existing_titles = set()


def scrape(url):
    r = requests.get(url)
    return r.text


def get_links(html):
    """
    Extracts links from the given HTML content and filters out certain types of links.
    :param html: The HTML content from which links will be extracted.
    :return: A list of unique links that start with '/Nyheder' or '/Video'.
    """
    print("Extracting links from html. . .")
    soup = BeautifulSoup(html, "html.parser")
    anchor_elements = soup.find_all('a')
    links = []

    for element in anchor_elements:
        href = element.get('href')
        if href and (href.startswith('/Nyheder') or href.startswith('/Video')):
            links.append(href)

    return list(dict.fromkeys(links))


def get_parsed_articles(links):
    """
    Retrieves parsed articles from the given list of links.

    :param links: A list of URLs to articles.

    :return: A list of parsed articles.
    """
    parsed_articles = []

    for url in links:
        article_url = base_url + url
        article_data = scrape(article_url)
        parsed_article = parse_article_content(article_data, article_url)
        parsed_articles.append(parsed_article)

    return parsed_articles


def parse_article_content(html, article_url):
    """
    Parse the content of an article from HTML.
    :param article_url: The URL of the article.
    :param html: The HTML content of the article.
    :return: An instance of the article class with parsed content.
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


def update_article_queue(new_articles):
    """
    Update the article queue with new articles.
app
    :param new_articles: a list of new articles to be added to the queue
    :return: None
    """
    if new_articles is None:
        return

    for new_article in new_articles:
        if fcb_news_queue.full():
            fcb_news_queue.get()
        fcb_news_queue.put(new_article)


def filter_existing_articles(imported_articles):
    """
    A function that filters out existing articles from a list of imported articles.

    :param imported_articles: a list of articles to filter

    :return: new_articles: a list of articles that are not already in existing_titles
    """

    if imported_articles is None:
        return

    new_articles = []
    for imported_article in imported_articles:
        if imported_article.title not in existing_titles:
            existing_titles.add(imported_article.title)
            new_articles.append(imported_article)

    return new_articles


def scrape_for_new_articles(existing_articles=None):
    """
    Scrapes for new articles from a base URL, parses them, filters out existing articles, updates the article queue, and returns the new articles.
    :return: new_articles: a list of articles that are not already in existing_titles
    """

    if existing_articles is not None:
        list(map(fcb_news_queue.put, existing_articles))

    print("Attempting to get articles")
    html = scrape(base_url + "/artikler")
    print("Scraped html. ")
    links = get_links(html)
    print("Found links")
    imported_articles = get_parsed_articles(links)
    print("Parsed articles, checking for duplicates. . .")
    new_articles = filter_existing_articles(imported_articles)
    update_article_queue(new_articles)
    return new_articles
