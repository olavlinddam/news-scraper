import time

from bs4 import BeautifulSoup
from selenium import webdriver


def get_page_source(url):
    options = webdriver.FirefoxOptions()
    driver = webdriver.Remote(
        command_executor='http://selenium:4444/wd/hub',  # Assuming Selenium server is running on localhost
        options=options
    )
    driver.get(url)
    page_source = driver.page_source
    time.sleep(5)
    driver.quit()
    return page_source


def scrape(url):
    page_source = get_page_source(url)
    soup = BeautifulSoup(page_source, 'html.parser')

    data_dict = {}

    popular_news = soup.find(class_="newsfeed newsfeed--popular").find_all(class_="article-card__headline")[:10]

    for news_item in popular_news:
        article_title = news_item.text.strip()
        href = news_item.get('href')
        data_dict[article_title] = href

    return data_dict
