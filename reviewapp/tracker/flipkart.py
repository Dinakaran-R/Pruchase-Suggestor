from bs4 import BeautifulSoup
import requests
import asyncio
import json
from .utility import get_headers, product_common_url


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



async def flipkart_reviews(url, ind = 1):

    if ind > 50:
        return

    response = requests.get(url, headers = await get_headers())
    htmldoc = response.content

    soup = BeautifulSoup(htmldoc, 'html.parser')

    reviews_list = soup.find('div', attrs={'class': '_1YokD2 _3Mn1Gg col-9-12'})

    count = ind
    for review in reviews_list.find_all('div', attrs={'class': '_1AtVbE col-12-12'}):
        # print(review)
        try:
            review = review.find('div', attrs = {'class' : 'col _2wzgFH K0kLPL'}).findChildren('div', attrs = {'class' : 'row'})
            print("\n")
            print(count, review[0].p.text, "\n" + review[1].text)

            # print(count, "Profile Name", review[2].p.text)
            # print(review[3])
            count += 1
        except Exception as e:
            print("Flipkart Reviews Exception 1:", e)

    try:
        if ind == 1:
            # print(url)
            if type(url[-1:]) == str:
                next_page = url + "&page=2"
            else:
                page_number = int(url[-1:]) + 1
                next_page = url[:-1] + str(page_number)
        else:
            next_page = soup.find_all("a", attrs={'class': '_1LKTO3'})[1]['href']
            next_page = "https://www.flipkart.com" + next_page

        print(next_page)
        await flipkart_reviews(next_page, ind + 10)

    except Exception as e:
        print("Flipkart Reviews Exception 2: ", e)
        # print(next_page)


async def get_flipkart_details(url):
    try:
        common_url = await product_common_url(url, "flipkart")
        response =  requests.get(common_url, headers = await get_headers())
        htmldoc = response.content
        soup = BeautifulSoup(htmldoc, 'html.parser')

        title = soup.find('span', attrs = {'class':'B_NuCI'}).text
        image = soup.find('div', attrs={'class': 'CXW8mj _3nMexc'}).img["src"]
        price = soup.find('div', attrs = {'class': '_30jeq3 _16Jk6d'}).text
        ratings = soup.find('div', attrs={'class': '_3LWZlK'}).text # or "_2d4LTz"
        ratings_count = soup.find('span', attrs={'class': '_2_R_DZ'}).text

        try:
            tag = soup.find('div', attrs={'class': '_220jKJ FEJ_PY'}).text
        except:
            tag = None

        # # rank_name = soup.find('span', attrs={'class': 'a-color-secondary a-size-base prodDetSectionEntry'}).text
        # info_table = soup.find('table', attrs = {'id' : 'productDetails_detailBullets_sections1'})
        # print(image)
        # print(title)
        # print(price)
        # print(ratings)
        # print(ratings_count)
        # print(tag)

        links = soup.find('div', attrs={'class': 'col JOpGWq'}).findChildren('a')

        # for url in reviews:
        #     print( "https://www.flipkart.com" + url['href'])

        reviews_url = "https://www.flipkart.com" + links[-1]['href']
        result = {"link": common_url, "title": title, "image": image, "merchant": "flipkart",
                  "price": price, "reviewsUrl" : reviews_url}

        return result

    except Exception as e:
        print(e)
        return False

    # await grab_reviews(all_reviews)

