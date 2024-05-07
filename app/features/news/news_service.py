from typing import List
from app.data.repository import Repository
from app.features.news.news_article import NewsArticle
from app.features.news.news_now_scraper import NewsNowScraper
import logging


class NewsService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)


    async def import_news(self, clubs_urls: dict) -> list[NewsArticle]:
        try:
            self.logger.info("Initializing news import...")
            
            all_imported_news = []

            for club_name, club_url in clubs_urls.items():
                dao = Repository("news", club_name)
                existing_news = await dao.get_latest_news(10)

                imported_news = NewsNowScraper(club_url).scrape(existing_news, club_name)
                new_articles = [article.to_dict() for article in imported_news]
                # all_imported_news.append(new_articles)
                
                if len(new_articles) != 0:
                    await dao.save_documents(new_articles)
                    all_imported_news.append(imported_news)

                
                
            if len(all_imported_news) == 0:
                logging.info("No new articles found. . .")
                return

            return all_imported_news
            # all_new_news_documents = []
            # for list_of_news in all_imported_news:
            #     new_news_documents = [article.to_dict() for article in list_of_news]
            #     all_new_news_documents.append(new_news_documents)
            #     await dao.save_documents(new_news_documents)

            # TODO: Add new news to the redis cache
            all_articles_flattened = [article for club_articles in all_imported_news for article in club_articles]
            return all_articles_flattened

        except Exception as e:
            self.logger.exception("Error scraping the latest news: %s", e)
            raise Exception("Could not scrape for new articles: " + str(e))

    async def get_existing_news(self, database_name, collection_name):
        try:
            repo = Repository(database_name, collection_name)
            sub = await repo.get_subscriber("https://www.foxnews.com")
            news_article_documents = await repo.get_latest_news(10)

            # Convert the MongoDB documents to news_article objects. This way we enforce validation
            news_articles = [NewsArticle.from_dict(news) for news in news_article_documents]

            # Convert the news_article objects to DTOs
            dto_list = [article.to_article_dto() for article in news_articles]

            return dto_list
        except Exception as e:
            self.logger.exception("Error getting existing articles", str(e))
            raise Exception("Could not get existing articles", str(e))

    @staticmethod
    def find_new_news(imported_news: list[NewsArticle], existing_news):
        existing_titles = {article['title'] for article in existing_news}

        new_news = []

        for item in imported_news:
            if item.title not in existing_titles:
                new_news.append(item)

        return new_news
