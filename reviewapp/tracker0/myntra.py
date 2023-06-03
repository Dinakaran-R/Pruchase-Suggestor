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


async def get_myntra_details(url):
    response =  requests.get(url,  headers = headers)
    htmldoc = response.content
    soup = BeautifulSoup(htmldoc, 'html.parser')

    for s in soup.find_all("script"):
        if 'pdpData' in s.text:
            script = s.get_text(strip=True)
            print(script)
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
    json_string = json.dumps(result)
    return True, json.loads(json_string)

# url = "https://www.myntra.com/kitchen-storage/milton/milton-pro-lunch-5pcs-black-tiffin--insulated-fabric-jacket-100ml-180ml-320ml-450ml-750ml/21779088/buy"
#
# asyncio.run(get_myntra_details(url))

