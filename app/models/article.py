from datetime import datetime


class article:
    def __init__(self, article_id: int, title: str, content: str, created_at: datetime, image_url: str, origin_url: str, video_url=None):
        self.article_id = article_id
        self.title = title
        self.content = content
        self.created_at = created_at
        self.image_url = image_url
        self.video_url = video_url
        self.origin_url = origin_url

