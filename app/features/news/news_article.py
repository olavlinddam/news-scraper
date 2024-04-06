from datetime import datetime

from app.features.news.news_article_dto import news_article_dto


class news_article:
    def __init__(self, title: str, created_at: str, url: str, article_id=None):
        self.article_id = article_id
        self.title = title
        self.created_at = created_at
        self.url = url
        self.validate()

    def validate(self):
        # Validate title
        if not self.title:
            raise ValueError("Title cannot be empty.")
        # Validate created_at
        try:
            datetime.strptime(self.created_at, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValueError("Invalid date format. Expected format: YYYY-MM-DD HH:MM:SS")
        # Validate url
        if not self.url.startswith("http://") and not self.url.startswith("https://"):
            raise ValueError("URL must start with http:// or https://")

    def to_dict(self):
        news_article_dict = {
            "title": self.title,
            "created_at": self.created_at,
            "url": self.url
        }
        if self.article_id:
            news_article_dict["article_id"] = self.article_id
        return news_article_dict

    def to_article_dto(self):
        return news_article_dto(self.title, self.url)


def from_dict(news):
    if news:
        return news_article(
            title=news.get("title", ""),
            created_at=news.get("created_at", ""),
            url=news.get("url", "")
        )
