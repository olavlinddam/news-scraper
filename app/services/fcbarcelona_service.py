import queue

from app.data.article_repository import save_news, get_news
from app.models.DTOs.fcbarcelona_news_dto import FCBarcelonaNewsDTO
from app.scrapers.news_now_scraper import scrape

barca_news_url = "https://www.newsnow.co.uk/h/Sport/Football/La+Liga/Barcelona?type=ts"
fcb_news_queue = queue.Queue(maxsize=10)
existing_titles = set()


def import_fcb_news():
    database_name = "news"
    collection_name = "fc_barcelona"

    try:
        if fcb_news_queue.empty():
            print("Queue is empty. . .")
            existing_news = get_news(database_name, collection_name, limit=10)

            if existing_news is not None:
                list(map(fcb_news_queue.put, existing_news))

        imported_news = scrape(barca_news_url)
        new_news = filter_existing_news(imported_news)
        update_news_queue(new_news)
        save_news(new_news, database_name, collection_name)

    except Exception as e:
        raise Exception("Could not scrape for new articles: " + str(e))


def get_existing_fcb_news():
    db_news = get_news("news", "fc_barcelona", 10)
    dto_list = []

    for news_item in db_news:
        dto = FCBarcelonaNewsDTO(
            title=news_item.get('title', ''),
            url=news_item.get('url', '')
        )
        dto_list.append(dto)

    return dto_list


def filter_existing_news(imported_news):
    """
    Filter out news articles that are already present in the fcb_news_queue.

    Parameters:
        imported_news (Dict[str, str]): A dictionary of imported news articles.

    Returns:
        new_news (Dict[str, str]): A dictionary of new news articles.
    """
    new_news = {}

    if imported_news is None:
        return new_news

    fcb_news_queue_list = list(fcb_news_queue.queue)
    fcb_news_queue_titles = set()
    for news in fcb_news_queue_list:
        if "title" in news and "url" in news:
            fcb_news_queue_titles.add(news["title"])

    for title, url in imported_news.items():
        if title not in fcb_news_queue_titles:
            new_news[title] = url

    return new_news


def update_news_queue(new_news):
    """
    Update the article queue with new articles.

    :param new_news: a dictionary of new articles to be added to the queue
    :return: None
    """
    if new_news is None:
        return

    for title, url in new_news.items():
        if fcb_news_queue.full():
            fcb_news_queue.get()
        fcb_news_queue.put({"title": title, "url": url})

