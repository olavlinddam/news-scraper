from datetime import datetime

from app.features.news.news_article_dto import NewsArticleDto


class NewsArticle:
    def __init__(self, club, title: str, created_at: str, url: str, article_id=None):
        self.article_id = article_id
        self.club = club
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
            "club": self.club,
            "title": self.title,
            "created_at": self.created_at,
            "url": self.url
        }
        if self.article_id:
            news_article_dict["article_id"] = self.article_id
        return news_article_dict

    def to_article_dto(self):
        return NewsArticleDto(self.title, self.url)

    @staticmethod
    def from_dict(news):
        if news:
            return NewsArticle(
                article_id=news.get("id", ""),
                club=news.get("club", ""),
                title=news.get("title", ""),
                created_at=news.get("created_at", ""),
                url=news.get("url", "")
            )
