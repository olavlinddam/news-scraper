import json
from typing import List
import redis
import logging

class redis_service:
    def __init__(self):
        self.r = redis.Redis(
            host='localhost',
            port=6379,
            decode_responses=True)
        
        self.logger = logging.getLogger(__name__)
        
    def cache_news_article(self, article_id: str, article_data: dict, expiration_time: int = 3600) -> None:
        """
        Caches a news article in Redis with a specified expiration time.

        Parameters:
        - article_id (str): The unique identifier for the article.
        - article_data (dict): The data of the article to be cached. This should be a dictionary.
        - expiration_time (int, optional): The time in seconds after which the cached article should expire. Defaults to 3600 seconds (1 hour).

        Returns:
        - None
        """
        article_data_json = json.dumps(article_data)
        self.r.set(article_id, article_data_json, ex=expiration_time)
        
    def get_latest_articles(self) -> List[str]:
        """
        Retrieves the latest 50 news articles from the Redis cache.

        Returns:
        - List[str]: A list of JSON strings representing the latest 50 news articles. Each string is a serialized version of the article data.
        """
        latest_articles = self.r.lrange('news_articles', 0, 49)
        return latest_articles