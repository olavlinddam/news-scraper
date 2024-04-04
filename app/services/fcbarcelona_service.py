from app.data.document_dao import document_dao
from app.models import news_article
from app.scrapers.news_now_scraper import scrape

barca_news_url = "https://www.newsnow.co.uk/h/Sport/Football/La+Liga/Barcelona?type=ts"


async def import_fcb_news():
    database_name = "news"
    collection_name = "fc_barcelona"

    try:
        dao = document_dao(database_name, collection_name)
        existing_news = await dao.get_documents(10)

        imported_news = scrape(barca_news_url)

        if len(existing_news) > 0:
            new_news = find_new_news(imported_news, existing_news)
            new_news_documents = [article.to_dict() for article in new_news]
        else:
            new_news = imported_news
            new_news_documents = [article.to_dict() for article in imported_news]

        await dao.save_documents(new_news_documents)

        # Push the new news to the subscribers
        new_news_dtos = []
        for new_news_article in new_news:
            news_dto = new_news_article.to_article_dto()
            new_news_dtos.append(news_dto)

    except Exception as e:
        raise Exception("Could not scrape for new articles: " + str(e))


async def get_existing_fcb_news():
    dao = document_dao("news", "fc_barcelona")
    news_article_documents = await dao.get_documents(10)

    # Convert the MongoDB documents to news_article objects. This way we enforce validation
    news_articles = [news_article.from_dict(news) for news in news_article_documents]

    # Convert the news_article objects to DTOs
    dto_list = [article.to_article_dto() for article in news_articles]

    return dto_list


def find_new_news(imported_news: list[news_article], existing_news):
    existing_titles = {article['title'] for article in existing_news}

    new_news = []

    for item in imported_news:
        if item.title not in existing_titles:
            new_news.append(item)

    return new_news
