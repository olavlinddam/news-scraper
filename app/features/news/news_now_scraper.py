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
    def __init__(self, url_to_scrape: str):
        self.compose_selenium_url = 'http://selenium:4444/wd/hub'
        self.standalone_selenium_url = 'http://localhost:4444/wd/hub'
        self.url_to_scrape = url_to_scrape
        self.driver = WebdriverManager().create_driver()
        self.logger = logging.getLogger(__name__)

    def get_page_source(self, driver):
        self.logger.info(f"Scraping: %s", self.url_to_scrape)
        driver.get(self.url_to_scrape)
        page_source = driver.page_source
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

        for popular_article in popular_articles:
            headline = popular_article.find('span', class_='article-title popular-title list-layout').text.strip()

            # Check if the headline is already in existing_news
            if any(article['title'] == headline for article in existing_news):
                continue  # Skip this iteration if the article is already in the database

            timestamp = popular_article.find('span', class_='article-publisher__timestamp').text.strip()
            href = popular_article.find('a', class_='article-card__headline')['href']

            # Resolve the redirect URL
            resolved_href = self.resolve_href(href)

            hours = int(timestamp[:-1])  # Remove the 'h' and convert to int
            article_created_at = datetime.now() - timedelta(hours=hours)
            article_created_at_str = article_created_at.strftime("%Y-%m-%d %H:%M:%S")
            article = NewsArticle(club, headline, article_created_at_str, resolved_href)
            news_articles.append(article)

        return news_articles

    def scrape(self, existing_news: list[dict[str, str]], club):
        """Scrapes for news articles and returns a list of imported news articles"""
        page_source = self.get_page_source(self.driver)
        soup = BeautifulSoup(page_source, 'html.parser')
        popular_articles = soup.find(class_="newsfeed newsfeed--popular").find_all(class_="article-card__inner")[:10]

        imported_news_articles = self.parse(popular_articles, existing_news, club)
        WebdriverManager().dispose_driver(self.driver)
        return imported_news_articles

# if __name__ == '__main__':
#     scraper = news_now_scraper('https://www.newsnow.co.uk/h/Sport/Football/La+Liga/Barcelona?type=ts')
#     scraper.scrape()
