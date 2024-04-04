from datetime import datetime, timedelta
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

from bs4 import BeautifulSoup
from selenium import webdriver

from app.models.news_article import news_article

compose_selenium_url = 'http://selenium:4444/wd/hub'
standalone_selenium_url = 'http://localhost:4444/wd/hub'

def get_page_source(url):
    options = webdriver.FirefoxOptions()
    driver = webdriver.Remote(
        command_executor=standalone_selenium_url,  # Assuming Selenium server is running on localhost
        options=options
    )
    driver.get(url)
    page_source = driver.page_source
    time.sleep(5)
    driver.quit()
    return page_source


def resolve_href(href):
    # Use Selenium to navigate to the original href and wait for the page to load
    options = webdriver.FirefoxOptions()
    driver = webdriver.Remote(
        command_executor=standalone_selenium_url,  # Assuming Selenium server is running on localhost
        options=options
    )
    driver.get(href)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    time.sleep(2)
    # Get the current URL after the page has loaded and any redirects have occurred
    resolved_href = driver.current_url
    driver.quit()
    return resolved_href


def parse(popular_articles):
    news_articles = []

    for popular_article in popular_articles:
        headline = popular_article.find('span', class_='article-title popular-title list-layout').text.strip()
        timestamp = popular_article.find('span', class_='article-publisher__timestamp').text.strip()
        href = popular_article.find('a', class_='article-card__headline')['href']

        # Resolve the redirect URL
        resolved_href = resolve_href(href)

        hours = int(timestamp[:-1])  # Remove the 'h' and convert to int
        article_created_at = datetime.now() - timedelta(hours=hours)
        article_created_at_str = article_created_at.strftime("%Y-%m-%d %H:%M:%S")
        article = news_article(headline, article_created_at_str, resolved_href)
        news_articles.append(article)

    return news_articles


def scrape(url):
    page_source = get_page_source(url)
    soup = BeautifulSoup(page_source, 'html.parser')
    popular_articles = soup.find(class_="newsfeed newsfeed--popular").find_all(class_="article-card__inner")[:10]

    imported_news_articles = parse(popular_articles)

    return imported_news_articles


if __name__ == '__main__':
    scrape("https://www.newsnow.co.uk/h/Sport/Football/La+Liga/Barcelona?type=ts")
