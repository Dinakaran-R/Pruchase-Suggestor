from bs4 import BeautifulSoup
import requests
import asyncio
import json

import random

headers = {
    'accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53',
    'Accept-Language': 'en-US,en;q=0.9,it;q=0.8,es;q=0.7',
    'referer': 'https://www.google.com/',
    'cookie': 'DSID=AAO-7r4OSkS76zbHUkiOpnI0kk-X19BLDFF53G8gbnd21VZV2iehu-w_2v14cxvRvrkd_NjIdBWX7wUiQ66f-D8kOkTKD1BhLVlqrFAaqDP3LodRK2I0NfrObmhV9HsedGE7-mQeJpwJifSxdchqf524IMh9piBflGqP0Lg0_xjGmLKEQ0F4Na6THgC06VhtUG5infEdqMQ9otlJENe3PmOQTC_UeTH5DnENYwWC8KXs-M4fWmDADmG414V0_X0TfjrYu01nDH2Dcf3TIOFbRDb993g8nOCswLMi92LwjoqhYnFdf1jzgK0'
}
# headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
# headers = requests.utils.default_headers()
# headers.update(
#     {
#         'User-Agent': 'My User Agent 1.0',
#     }
# )
#
# headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}


user_agents = [
  "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
  "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
  "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0"
  ]


count = 1
def remove_spaces(text):
    return " ".join(text.split())

# Dina Added : #1/6
reviews_for_sentiment = []

async def grab_reviews(url, ind):
    # random_user_agent = random.choice(user_agents)
    # headers = {
    #     'User-Agent': random_user_agent
    # }

    response = requests.get(url, headers = headers)
    htmldoc = response.content

    # print(response.status_code)

    soup = BeautifulSoup(htmldoc, 'html.parser')
    # print(soup.prettify())

    reviews_list = soup.find('div', attrs={'id': 'cm_cr-review_list'})
    # print(reviews_list)
    reviews_header = reviews_list.h3.text
    reviews_header = remove_spaces(reviews_header)

    print(reviews_header)

    count = ind
    # get all the reviews in list for sentiment analysis

    # Dina Added : #2/6
    global reviews_for_sentiment

    for review in reviews_list.find_all('div', attrs={'class': 'a-row'}):
        # print(review)
        try:
            profile_name = review.find('span', attrs={'class': 'a-profile-name'}).text
            review_title = review.find('a', attrs={'data-hook': 'review-title'}).text
            review_body  = review.find('span', attrs={'data-hook': 'review-body'}).text

            profile_name = remove_spaces(profile_name)
            review_title = remove_spaces(review_title)
            review_body = remove_spaces(review_body)

            print(count, "Profile Name: " + profile_name, "\n" + review_title, ":", review_body)

            #appending the review (append both review title and review body)

            # Dina Added : #3/6
            reviews_for_sentiment.append(review_title +" "+ review_body)
            count += 1

        except Exception as e:
            # print(e)
            pass

    # Dina Added : #4/6
    print("Reviews List : ",reviews_for_sentiment)

    # get next page
    try:
        pagination_bar = soup.find('div', attrs={'id': 'cm_cr-pagination_bar'})
        # print(pagination_bar)
        next_page = pagination_bar.find("li", attrs={'class': 'a-last'}).a['href']
        next_page = "https://www.amazon.in" + next_page
        print(next_page)

        # while loop to go to next page. increase the integer to increase pages(eg. ind<2, ind<5)

        # Dina Added : #5/6
        while ind<2:
            await grab_reviews(next_page, count)
            ind+=1

    except Exception as e:
        pass
        # "a-disabled a-last"


async def get_product_details(url):
    response =  requests.get(url,  headers = headers)

    print("Response Code : ",response.status_code)

    htmldoc = response.content

    soup = BeautifulSoup(htmldoc, 'html.parser')
    # soup = BeautifulSoup(r.content, 'html5lib')

    # print(soup.prettify())
    image = soup.find('img', attrs={'id': 'landingImage'})
    title = soup.find('span', attrs = {'id':'productTitle'}).text
    price = soup.find('span', attrs = {'class': 'a-offscreen'}).text
    info_table = soup.find('table', attrs = {'id' : 'productDetails_detailBullets_sections1'})

    title = remove_spaces(title)
    price = remove_spaces(price)
    image = image["data-old-hires"] #image["src"] #image["data-a-dynamic-image"]
    # print(ratings)
    # print(ratings_count)
    # print(rank_name)

    for row in info_table.findAll('tr'):
        head = row.find('th').text
        value = row.find('td').text

        head = remove_spaces(head)
        value = remove_spaces(value)

        print(head, " : ", value)

        # To get corresponding bestsellers page

        # if "Best Sellers Rank" == head:
        #     try:
        #         print("https://www.amazon.in" + row.find('td').a['href'])
        #     except:
        #         pass

        if "Date First Available" == head:
            break

    all_reviews = soup.find('div', attrs={'id': 'reviews-medley-footer'})
    all_reviews = all_reviews.find('div', attrs={'class': 'a-row a-spacing-medium'})

    reviews_url = "https://www.amazon.in" + all_reviews.a['href']
    print(all_reviews.a.text, " : ", reviews_url)

    result = {"link": reviews_url, "title": title, "image" : image, "merchant" : "amazon", "price" : price}
    # print(json.dumps(result))
    json_string = json.dumps(result)

    await grab_reviews(reviews_url, 1)

    return True, json.loads(json_string)


#asyncio.run(get_product_details("https://amzn.eu/d/arWl7U2"))

# asyncio.run(grab_reviews("https://www.amazon.in/realme-Segment-Fastest-Charging-High-res/product-reviews/B0BZ466BWW/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews", 1))

# get_product_details("https://dl.flipkart.com/s/oUWWOpuuuN")
# get_product_details("https://www.flipkart.com/hp-pavilion-ryzen-5-hexa-core-5625u-16-gb-512-gb-ssd-windows-11-home-14-ec1005au-thin-light-laptop/p/itmec3d94a599fc0?pid=COMGHQ3NWPPAPYF4&lid=LSTCOMGHQ3NWPPAPYF4UDJA9S&marketplace=FLIPKART&store=6bo%2Fb5g&srno=b_1_1&otracker=hp_omu_Best%2Bof%2BElectronics_1_3.dealCard.OMU_96TCV7E0HFS8_3&otracker1=hp_omu_PINNED_neo%2Fmerchandising_Best%2Bof%2BElectronics_NA_dealCard_cc_1_NA_view-all_3&fm=neo%2Fmerchandising&iid=en_RaRFpSL%2FU6SQ36Om4Z8qUc2y0gOTz1g9t4HrvPij6S7yxwMOj32mirAH8jVkuBXxj0qjqb6sK%2BExAdnx%2FGvkmQ%3D%3D&ppt=dynamic&ppn=LOYALTY_PAGE&ssid=dtwj5pzj3k0000001683098252171")