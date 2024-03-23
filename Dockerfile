#
FROM python:3.9-slim

#
WORKDIR /news-scraper

#
COPY ./requirements.txt /news-scraper/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /news-scraper/requirements.txt

#
COPY ./app /news-scraper/app

#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]