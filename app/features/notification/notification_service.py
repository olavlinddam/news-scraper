import json
import logging
from typing import Any, Dict, List

import requests

from app.features.news.news_article import NewsArticle
from app.features.news.news_article_dto import NewsArticleDTO


class NotificationService:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def push(self, documents: List[NewsArticle], subscribers: List[Dict[str, Any]]) -> None:
        if not documents or not subscribers:
            return

        for subscriber in subscribers:
            clubs_subscribed_to = subscriber['subscribed_to']
            relevant_documents = [doc for doc in documents if doc.club in clubs_subscribed_to]
            dtos = []
            for document in relevant_documents:
                dto = NewsArticleDTO(document).to_dict()
                dtos.append(dto)

            if not relevant_documents:
                continue

            self.logger.info(f"Sending {len(relevant_documents)} documents to {subscriber['url']}")
            data = json.dumps(dtos)

            try:
                response = requests.post(subscriber['url'], data=data, headers={'Content-Type': 'application/json'})
                response.raise_for_status()  # Raises an HTTPError if the response status code is 4xx or 5xx
                print(f"Successfully sent {len(relevant_documents)} documents to {subscriber['url']}")
            except requests.exceptions.HTTPError as e:
                print(f"HTTP Error: {e}")
            except requests.exceptions.ConnectionError as e:
                print(f"Error Connecting: {e}")
            except requests.exceptions.Timeout as e:
                print(f"Timeout Error: {e}")
            except requests.exceptions.RequestException as e:
                print(f"Something went wrong: {e}")