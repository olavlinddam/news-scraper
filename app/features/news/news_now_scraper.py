import time
import logging

from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.features.news.news_article import NewsArticle
from app.features.news.webdriver_manager import WebdriverManager


class NewsNowScraper:
    def __init__(self):
        self.compose_selenium_url = 'http://selenium:4444/wd/hub'
        self.standalone_selenium_url = 'http://localhost:4444/wd/hub'
        self.driver = WebdriverManager().create_driver()
        self.logger = logging.getLogger(__name__)

    def get_page_source(self, url_to_scrape):
        self.logger.info(f"Scraping: %s", url_to_scrape)
        self.driver.get(url_to_scrape)
        page_source = self.driver.page_source
        time.sleep(5)
        return page_source

    def resolve_href(self, href):
        # Use Selenium to navigate to the original href and wait for the page to load
        self.driver.get(href)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        time.sleep(2)

        # Get the current URL after the page has loaded and any redirects have occurred
        resolved_href = self.driver.current_url
        return resolved_href

    def parse(self, popular_articles, existing_news, club):
        """Parses the news articles and returns a list of news articles"""
        self.logger.info(f"Parsing page source.")

        news_articles = []

        self.logger.info("Filtering existing articles from the imported articles.")
        for popular_article in popular_articles:

            headline = popular_article.find('span', class_='article-title popular-title list-layout').text.strip()

            # Check if the headline is already in existing_news
            if any(article['title'] == headline for article in existing_news):
                continue  # Skip this iteration if the article is already in the database

            # Find the article link and resolve the redirect URL
            href = popular_article.find('a', class_='article-card__headline')['href']
            resolved_href = self.resolve_href(href)

            timestamp = self.extract_and_format_timestamp(popular_article)
            article = NewsArticle(club, headline, timestamp, resolved_href)
            news_articles.append(article)

        self.logger.info(f"Found {len(news_articles)} news articles.")
        return news_articles

    def scrape(self, existing_news: list[dict[str, str]], club, url_to_scrape: str):
        """Scrapes for news articles and returns a list of imported news articles"""

        page_source = self.get_page_source(url_to_scrape)
        soup = BeautifulSoup(page_source, 'html.parser')
        popular_articles = soup.find(class_="newsfeed newsfeed--popular").find_all(class_="article-card__inner")[:10]
        imported_news_articles = self.parse(popular_articles, existing_news, club)
        return imported_news_articles

    def dispose_driver(self):
        WebdriverManager().dispose_driver(self.driver)

    @staticmethod
    def extract_and_format_timestamp(popular_article):
        timestamp = popular_article.find('span', class_='article-publisher__timestamp').text.strip()
        hours = int(timestamp[:-1])  # Remove the 'h' and convert to int
        article_created_at = datetime.now() - timedelta(hours=hours)
        article_created_at_str = article_created_at.strftime("%Y-%m-%d %H:%M:%S")
        return article_created_at_str

# if __name__ == '__main__':
#     scraper = news_now_scraper('https://www.newsnow.co.uk/h/Sport/Football/La+Liga/Barcelona?type=ts')
#     scraper.scrape()
