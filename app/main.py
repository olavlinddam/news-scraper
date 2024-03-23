from fastapi import FastAPI, Depends
from .dependencies import get_query_token
from app.api.news import router

app = FastAPI(dependencies=[Depends(get_query_token)])

app.include_router(router)
