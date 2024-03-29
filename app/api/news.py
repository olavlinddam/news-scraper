from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_db_connection, get_token_header
from app.models.article import article
from app.services.scrapers.fcbarcelona.fcbarcelonadk import scrape_and_parse_articles
from app.services.summarizer import summarize
from app.data.article_repository import save_articles, get_articles
import uvicorn

from pymongo import MongoClient

router = APIRouter(
    prefix="/news",
    tags=["news"],
    #dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


# Dependency for injecting the collection object
async def get_articles_collection():
    return Depends(get_db_connection)  # Reuse the get_db_connection function


# region endpoints

@router.get("/scrape")
async def scrape():
    database_name = "articles"
    collection_name = "fc_barcelona"

    # articles_full_content = scrape_and_parse_articles()
    # articles_with_summary = summarize(articles_full_content)
    # save_articles(articles_with_summary, database_name, collection_name)

    test_article = article(
        title="The Importance of JSON in Web Development",
        content="JSON (JavaScript Object Notation) is a lightweight data interchange format...",
        created_at="2022-01-01",
        origin_url="https://example.com/json-article"
    )
    dict_article = test_article.to_dict()
    save_articles(dict_article, database_name, collection_name)
# endregion


if __name__ == "__main__":
    uvicorn.run("app.api.news:router", host="0.0.0.0", port=8000)