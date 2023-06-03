from bs4 import BeautifulSoup
import requests
import asyncio
import json

headers = {
    'accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53',
    'Accept-Language': 'en-US,en;q=0.9,it;q=0.8,es;q=0.7',
    'referer': 'https://www.google.com/',
    'cookie': 'DSID=AAO-7r4OSkS76zbHUkiOpnI0kk-X19BLDFF53G8gbnd21VZV2iehu-w_2v14cxvRvrkd_NjIdBWX7wUiQ66f-D8kOkTKD1BhLVlqrFAaqDP3LodRK2I0NfrObmhV9HsedGE7-mQeJpwJifSxdchqf524IMh9piBflGqP0Lg0_xjGmLKEQ0F4Na6THgC06VhtUG5infEdqMQ9otlJENe3PmOQTC_UeTH5DnENYwWC8KXs-M4fWmDADmG414V0_X0TfjrYu01nDH2Dcf3TIOFbRDb993g8nOCswLMi92LwjoqhYnFdf1jzgK0'
}

def remove_spaces(text):
    return " ".join(text.split())

async def generate_links(url):
    page_number = int(url[-1:]) + 1
    next_page = url[:-1] + str(page_number)

    pages = []

    pages.append(url)
    pages.append(next_page)

    for i in range(page_number + 1, 1000):
        ind = next_page.rfind(str(i - 1))
        next_page = next_page[:ind] + str(i)
        pages.append(next_page)

    i = 0
    for url in pages:
        asyncio.create_task(grab_reviews(url, i))
        # i += 10



async def grab_reviews(url, ind):

    response = requests.get(url, headers = headers)
    htmldoc = response.content

    # print(response.status_code)

    soup = BeautifulSoup(htmldoc, 'html.parser')

    # try:
    #     if ind == 0:
    #         page_number = int(url[-1:]) + 1
    #         next_page = url[:-1] + str(page_number)
    #     else:
    #         next_page = soup.find_all("a", attrs={'class': '_1LKTO3'})[1]['href']
    #         next_page = "https://www.flipkart.com" + next_page
    #
    #     print(next_page)
    #     await grab_reviews(next_page, ind + 10)
    #
    # except Exception as e:
    #     print("In Next Page, Exception: ", e)
    #     print(next_page)
    #     pass
    #     # "a-disabled a-last"


    reviews_list = soup.find('div', attrs={'class': '_1YokD2 _3Mn1Gg col-9-12'})
    # print(reviews_list)
    # reviews_header = reviews_list.h3.text
    # reviews_header = remove_spaces(reviews_header)
    #
    # print(reviews_header)

    count = ind + 1
    for review in reviews_list.find_all('div', attrs={'class': '_1AtVbE col-12-12'}):
        # print(review)
        try:
            review = review.find('div', attrs = {'class' : 'col _2wzgFH K0kLPL'}).findChildren('div', attrs = {'class' : 'row'})
            print("\n")
            print(count, "Profile Name", review[2].p.text)
            print(review[0].p.text)
            print(review[1].text)
            # print(review[3])
            count += 1
        except Exception as e:
            print("Loop Exception:", e)
            pass


async def get_snapdeal_details(url):
    response =  requests.get(url,  headers = headers)
    htmldoc = response.content
    soup = BeautifulSoup(htmldoc, 'html.parser')

    title = soup.find('h1', attrs = {'itemprop':'name'}).text
    image = soup.find('img', attrs={'slidenum': '0'})["bigsrc"]
    price = soup.find('span', attrs={'class': 'pdp-final-price'}).text
    ratings = soup.find('span', attrs={'class': 'avrg-rating'}).text #rating
    ratings_count = soup.find('span', attrs={'class': 'total-rating showRatingTooltip'}).text #total-review-txt


    title = remove_spaces(title)
    price = remove_spaces(price)

    result = {"link": response.url, "title": title, "image": image, "merchant": "snapdeal", "price": price}
    json_string = json.dumps(result)
    return True, json.loads(json_string)


url = "https://www.snapdeal.com/product/aqua-grand-15-ltr-ro/626708147604#bcrumbLabelId:3631"

asyncio.run(get_snapdeal_details(url))
