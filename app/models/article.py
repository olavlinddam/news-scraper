from datetime import datetime


class article:
    def __init__(self, title: str, content: str, created_at: str, origin_url: str, video_url=None, article_id=None):
        self.article_id = article_id
        self.title = title
        self.content = content
        self.created_at = created_at
        self.video_url = video_url
        self.origin_url = origin_url

    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at,
            "origin_url": self.origin_url,
            "video_url": self.video_url,
            "article_id": self.article_id
        }
