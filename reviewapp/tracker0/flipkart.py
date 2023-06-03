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


async def get_flipkart_details(url):
    response =  requests.get(url,  headers = headers)
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

    all_reviews = "https://www.flipkart.com" + links[-1]['href']
    result = {"link": response.url, "title": title, "image": image, "merchant": "flipkart", "price": price}
    json_string = json.dumps(result)
    return True, json.loads(json_string)

    # await grab_reviews(all_reviews, 1)

asyncio.run(get_flipkart_details("https://www.flipkart.com/samsung-galaxy-f23-5g-aqua-blue-128-gb/p/itm89d3030e3857e?pid=MOBGBKQFHKZHTHKJ&lid=LSTMOBGBKQFHKZHTHKJ7WW16A&marketplace=FLIPKART&store=tyy%2F4io&spotlightTagId=FkPickId_tyy%2F4io&srno=b_1_4&otracker=hp_omu_Top%2BOffers_1_4.dealCard.OMU_TOO4ENUDCC8Q_4&otracker1=hp_omu_PINNED_neo%2Fmerchandising_Top%2BOffers_NA_dealCard_cc_1_NA_view-all_4&fm=neo%2Fmerchandising&iid=90156599-c02b-4729-9d06-9a95b95458a1.MOBGBKQFHKZHTHKJ.SEARCH&ppt=browse&ppn=browse"))

# asyncio.run(get_flipkart_details("https://www.flipkart.com/samsung-galaxy-f23-5g-aqua-blue-128-gb/p/itme54bc0c2292f4?pid=MOBGBKQF45XPEUHA&lid=LSTMOBGBKQF45XPEUHAYAHBJE&marketplace=FLIPKART&store=tyy%2F4io&srno=b_1_1&otracker=hp_omu_Top%2BOffers_1_4.dealCard.OMU_TOO4ENUDCC8Q_4&otracker1=hp_omu_PINNED_neo%2Fmerchandising_Top%2BOffers_NA_dealCard_cc_1_NA_view-all_4&fm=neo%2Fmerchandising&iid=90156599-c02b-4729-9d06-9a95b95458a1.MOBGBKQF45XPEUHA.SEARCH&ppt=hp&ppn=homepage&ssid=e18lddk7n40000001683195757201"))

# asyncio.run(grab_reviews("https://www.flipkart.com/samsung-galaxy-f23-5g-aqua-blue-128-gb/product-reviews/itme54bc0c2292f4?pid=MOBGBKQF45XPEUHA&lid=LSTMOBGBKQF45XPEUHAYAHBJE&marketplace=FLIPKART&page=1", 0))

url = "https://www.flipkart.com/samsung-galaxy-f23-5g-aqua-blue-128-gb/product-reviews/itme54bc0c2292f4?pid=MOBGBKQF45XPEUHA&lid=LSTMOBGBKQF45XPEUHAYAHBJE&marketplace=FLIPKART&page=1"
# asyncio.run(generate_links(url))