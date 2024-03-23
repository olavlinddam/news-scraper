from datetime import datetime
from random import randint
from random import choices
from typing import List


from ..models.article import article


def generate_articles(num_articles: int) -> List[article]:
    """Generates a list of articles with random titles and content.

    Args:
        num_articles: The number of articles to generate.

    Returns:
        A list of Article objects.
    """

    articles = []
    fake_titles = [
        "Barcelona Dominates Against Real Madrid",
        "Messi Scores Another Hat-Trick!",
        "La Liga Race Heats Up as Teams Battle for Top Spot",
        "FC Barcelona Unveils New Stadium Plans",
        "Transfer Rumors: Who Will Join Barcelona Next?",
        "Barcelona Youth Academy Produces Rising Star",
        "Barcelona Legend Shares Inspiring Story",
        "Fans Celebrate Barcelona's Historic Victory",
        "Barcelona Makes Statement in Champions League",
        "FC Barcelona Partners with Sustainability Initiative"
    ]
    fake_content = [
        "Barcelona secured a convincing victory against Real Madrid...",
        "Lionel Messi once again showcased his brilliance...",
        "The race for the La Liga title intensifies...",
        "FC Barcelona unveiled plans for a state-of-the-art...",
        "Transfer rumors swirl around several potential signings...",
        "A young talent from La Masia impresses on the field...",
        "A Barcelona legend shares his journey and inspires the next...",
        "Thousands of fans erupt in celebration after a thrilling match...",
        "Barcelona dominates their Champions League group stage...",
        "FC Barcelona partners with a leading organization to promote..."
    ]

    for i in range(num_articles):
        article_id = i
        random_title_index = randint(0, len(fake_titles) - 1)
        random_content_index = randint(0, len(fake_content) - 1)
        random_title = choices(fake_titles, k=1)[0]  # Choose 1 random title
        new_article = article(
            article_id=article_id,
            title=random_title,
            content=fake_content[random_content_index],
            created_at=datetime.now(),
            image_url="https://example.com/placeholder.jpg",  # Placeholder image
            origin_url="https://www.example.com/sports/barcelona-news",
            video_url=None
        )
        articles.append(new_article)
    return articles