from app.data.repository import repository
from app.features.news.news_article import news_article
from app.features.news.news_now_scraper import news_now_scraper as scraper
import logging


class news_service:
    def __init__(self, database_name: str, collection_name: str, url_to_scrape: str = None):
        self.database_name = database_name
        self.collection_name = collection_name
        self.repository = repository(self.database_name, self.collection_name)
        self.logger = logging.getLogger(__name__)
        self.url_to_scrape = url_to_scrape
        self.scraper = self.get_news_now_scraper()


    def get_news_now_scraper(self):
        if self.url_to_scrape:
            return scraper(self.url_to_scrape)

    async def import_news(self):
        try:
            self.logger.info("Initializing news import for " + self.collection_name)
            dao = repository(self.database_name, self.collection_name)
            existing_news = await dao.get_latest_news(10)

            imported_news = self.scraper.scrape(existing_news)

            if not imported_news:
                logging.info("No new articles found. . .")
                return

            new_news_documents = [article.to_dict() for article in imported_news]
            await dao.save_documents(new_news_documents)

            # TODO: Add new news to the redis cache

            # Push the new news to the subscribers
            # new_news_dtos = []
            # for new_news_article in imported_news:
            #     news_dto = new_news_article.to_article_dto()
            #     new_news_dtos.append(news_dto)

        except Exception as e:
            self.logger.exception("Error scraping the latest news: %s", e)
            raise Exception("Could not scrape for new articles: " + str(e))

    async def get_existing_news(self):
        try:
            repo = repository(self.database_name, self.collection_name)
            sub = await repo.get_subscriber("https://www.foxnews.com")
            news_article_documents = await repo.get_latest_news(10)

            # Convert the MongoDB documents to news_article objects. This way we enforce validation
            news_articles = [news_article.from_dict(news) for news in news_article_documents]

            # Convert the news_article objects to DTOs
            dto_list = [article.to_article_dto() for article in news_articles]

            return dto_list
        except Exception as e:
            self.logger.exception("Error getting existing articles", str(e))
            raise Exception("Could not get existing articles", str(e))

    @staticmethod
    def find_new_news(imported_news: list[news_article], existing_news):
        existing_titles = {article['title'] for article in existing_news}

        new_news = []

        for item in imported_news:
            if item.title not in existing_titles:
                new_news.append(item)

        return new_news
