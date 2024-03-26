from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_token_header, get_db_connection
from ..data.fake_news_db import generate_articles
from pymongo import MongoClient

router = APIRouter(
    prefix="/news",
    tags=["news"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


# Dependency for injecting the collection object
async def get_articles_collection():
    return Depends(get_db_connection)  # Reuse the get_db_connection function


fake_news = generate_articles(10)


# region endpoints
@router.get("/")
async def get_news():
    return fake_news


@router.get("/db-test")
async def get_all_articles(articles: MongoClient = Depends(get_articles_collection)):
    # Use the articles collection object for database operations
    all_articles = articles.find({})  # Example query
    return all_articles  # Return the results


@router.get("/{article_id}")
async def get_article(article_id: int):
    if not article_id.is_integer():
        raise HTTPException(status_code=400, detail="Article id must be an integer")
    for article in fake_news:
        if article.article_id == article_id:
            return article

# @router.post("/")
# async def create_article(article: str):
#     """Creates a new article and adds it to the fake_news_db.
#
#         Args:
#             article: The content of the new article (as a string).
#
#         Returns:
#             A JSON response with the newly created article details
#             and its automatically generated ID.
#         """
#
#     # Generate a unique ID for the new article
#     new_article_id = f"{len(fake_news_db) + 1}"
#
#     # Add the new article to the database
#     fake_news_db[new_article_id] = article
#
#     # Return the newly created article details
#     return {
#         "message": "Article created successfully!",
#         "article": fake_news_db[new_article_id],
#         "article_id": new_article_id,
#     }
# endregion
