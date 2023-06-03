from bs4 import BeautifulSoup
import requests
import asyncio
import json

from .utility import remove_spaces, get_headers

async def get_snapdeal_details(url):
    try:
        response =  requests.get(url,  headers = await get_headers)
        htmldoc = response.content
        soup = BeautifulSoup(htmldoc, 'html.parser')

        title = soup.find('h1', attrs = {'itemprop':'name'}).text.strip()
        image = soup.find('img', attrs={'slidenum': '0'})["bigsrc"]
        price = soup.find('span', attrs={'class': 'pdp-final-price'}).text.strip()
        ratings = soup.find('span', attrs={'class': 'avrg-rating'}).text #rating
        ratings_count = soup.find('span', attrs={'class': 'total-rating showRatingTooltip'}).text #total-review-txt

        # title = remove_spaces(title)
        # price = remove_spaces(price)

        result = {"link": response.url, "title": title, "image": image, "merchant": "snapdeal", "price": price}
        return result
    except Exception as e:
        print(e)
        return False

