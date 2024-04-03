from app.dependencies import get_db_connection


async def get_subscribers(collection_name: str):



    db_connection = get_db_connection("subscribers", collection_name)
    subscribers_cursor = db_connection.find({})
    subscribers = [subscriber for subscriber in subscribers_cursor]
    return subscribers
