from app.data.models.news_article import NewsArticle


class NewsArticleDTO:
    def __init__(self, news_article: NewsArticle):
        self.club = news_article.club
        self.title = news_article.title
        self.created_at = news_article.created_at
        self.url = news_article.url

    def to_dict(self):
        article_push_request_dict = {
            "club": self.club,
            "title": self.title,
            "created_at": self.created_at,
            "url": self.url
        }
        return article_push_request_dict
