import json
from app.dependencies import get_db_connection


def save_articles(articles, database_name, collection_name):
    db_connection = get_db_connection(database_name, collection_name)

    for article in articles:
        # Convert the article object to JSON
        article_json = json.dumps(article.__dict__)

        # Save the article to the database
        db_connection.insert_one(json.loads(article_json))


def get_articles(database_name, collection_name):
    db_connection = get_db_connection(database_name, collection_name)
    articles_cursor = db_connection.find({})
    db_articles = [article for article in articles_cursor]
    for a in db_articles:
        print(a)
    return db_articles


if __name__ == "__main__":
    articles = get_articles("articles", "fc_barcelona")
