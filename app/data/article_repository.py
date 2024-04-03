import json
from app.dependencies import get_db_connection


def save_news(news, database_name, collection_name):
    """
    Save a list of articles to a specified database and collection.

    Parameters:
        news (Dict[str, str]): A dictionary of news data
        database_name (str): The name of the database to save the articles to.
        collection_name (str): The name of the collection within the database to save the articles to.

    Returns:
        None
    """
    db_connection = get_db_connection(database_name, collection_name)

    if news:
        # Transform the news data into a list of dictionaries
        news_list = [{"title": title, "url": url} for title, url in news.items()]
        db_connection.insert_many(news_list, ordered=True)


def get_news(database_name, collection_name, limit):
    db_connection = get_db_connection(database_name, collection_name)
    news_cursor = db_connection.find({}).limit(limit)
    db_news = [news for news in news_cursor]
    return db_news
