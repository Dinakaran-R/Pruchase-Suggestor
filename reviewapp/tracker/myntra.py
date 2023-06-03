from bs4 import BeautifulSoup
import requests
import asyncio
import json
from .utility import get_headers

async def get_myntra_details(url):
    try:
        response =  requests.get(url,  headers = await get_headers())
        if response.status_code != 200:
            return None
        htmldoc = response.content
        soup = BeautifulSoup(htmldoc, 'html.parser')
        for s in soup.find_all("script"):
            if 'pdpData' in s.text:
                script = s.get_text(strip=True)
                # print(script)
                json_dict = json.loads(script[script.index('{'):])
                details = json_dict["pdpData"]
                title = details["name"]
                price = details["price"]["discounted"]
                url = "https://www.myntra.com/" + details["landingPageUrl"] # response.url
                ratings = details["ratings"]["averageRating"]
                ratings_count = details["ratings"]["totalCount"]
                image = details["media"]["albums"][0]["images"][0]["imageURL"]

                # print(details["tagData"])
                # print(details["tags"])
                # print(details["productDetails"])

                # for i in details:
                #     print(i)
                #
                # print(details)
                break
        result = {"link": response.url, "title": title, "image": image, "merchant": "myntra", "price": price}
        # json_string = json.dumps(result)
        # return json.loads(json_string)

        return result

    except Exception as e:
        print(e)
        return False



