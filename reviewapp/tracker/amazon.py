from bs4 import BeautifulSoup
import requests
import asyncio
import json
from ..sentiment.sentiment import get_sentiment

from .utility import remove_spaces, get_headers, product_common_url

# headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
# headers = requests.utils.default_headers()
# headers.update(
#     {
#         'User-Agent': 'My User Agent 1.0',
#     }
# )
#
# headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}


# user_agents = [
#   "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
#   "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0",
#   "Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0"
#   ]


# random_user_agent = random.choice(user_agents)
# headers = {
#     'User-Agent': random_user_agent
# }


# Dina Added : #1/6


async def amazon_reviews(url,reviews_for_sentiment = [], ind = 1):

    if ind > 50:
        return

    response = requests.get(url, headers = await get_headers())
    htmldoc = response.content

    # print(response.status_code)

    soup = BeautifulSoup(htmldoc, 'html.parser')
    # print(soup.prettify())

    reviews_list = soup.find('div', attrs={'id': 'cm_cr-review_list'})
    # print(reviews_list)
    reviews_header = reviews_list.h3.text
    reviews_header = remove_spaces(reviews_header)

    print(reviews_header)

    # Dina Added : #2/6
    # global reviews_for_sentiment

    count = ind
    for review in reviews_list.find_all('div', attrs={'class': 'a-row'}):
        # print(review)
        try:
            # profile_name = review.find('span', attrs={'class': 'a-profile-name'}).text
            review_title = review.find('a', attrs={'data-hook': 'review-title'}).text
            review_body  = review.find('span', attrs={'data-hook': 'review-body'}).text

            # profile_name = remove_spaces(profile_name)
            review_title = remove_spaces(review_title)
            review_body = remove_spaces(review_body)

            print(count, review_title, "\n" + review_body)

            # Dina Added : #3/6
            reviews_for_sentiment.append(review_title + " " + review_body)

            count += 1

        except Exception as e:
            # print("Amazon Reviews Exception 1: ", e)
            pass

    try:
        pagination_bar = soup.find('div', attrs={'id': 'cm_cr-pagination_bar'})
        # print(pagination_bar)
        next_page = pagination_bar.find("li", attrs={'class': 'a-last'}).a['href']
        next_page = "https://www.amazon.in" + next_page
        print(next_page)
        await amazon_reviews(next_page, reviews_for_sentiment, count)


    except Exception as e:
        print("Amazon Review Error : ",e)
        # print("Amazon Reviews Exception 2: ", e)
        # "a-disabled a-last"
    # Dina Added : #4/6
    print("Reviews List : ", reviews_for_sentiment)

    return reviews_for_sentiment


async def get_amazon_details(url):
    try:
        common_url = await product_common_url(url, "amazon")
        response = requests.get(common_url,  headers = await get_headers())

        # print(response.status_code)
        # print(common_url)
        # print(response.url)
        # print(response.is_redirect)
        # print(response.is_permanent_redirect)

        # print(response.json)
        # print(response.links)
        # print(response.headers)

        htmldoc = response.content

        soup = BeautifulSoup(htmldoc, 'html.parser')
        # soup = BeautifulSoup(r.content, 'html5lib')

        # print(soup.prettify())
        image = soup.find('img', attrs={'id': 'landingImage'})
        title1 = soup.find('span', attrs = {'id':'productTitle'})
        title2 = soup.select_one('#prologueProductTitle')

        price1 = soup.select_one("span.a-price.a-text-price.a-size-medium.apexPriceToPay > span:nth-child(2)")
        price2 = soup.select_one("span.a-price.aok-align-center.priceToPay > span.a-offscreen")

        # price_span = soup.find('span',
        #      attrs={'class': 'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'})
        # price = price_span.find('span', attrs = {'class': 'a-offscreen'}).text
        # ratings = soup.find('span', attrs={'id': 'acrPopover'})['title']
        # ratings_count = soup.find('span', attrs={'id': 'acrCustomerReviewText'}).text
        # rank_name = soup.find('span', attrs={'class': 'a-color-secondary a-size-base prodDetSectionEntry'}).text
        info_table = soup.find('table', attrs = {'id' : 'productDetails_detailBullets_sections1'})

        title = (title1 or title2).text.strip()
        price = (price1 or price2).text.strip()
        image = image["data-old-hires"] #image["src"] #image["data-a-dynamic-image"]
        # print(ratings)
        # print(ratings_count)
        # print(rank_name)


        if info_table != None:
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

        result = { "link": common_url, "title": title, "image" : image, "merchant" : "amazon",
                   "price" : price, "reviewsUrl" : reviews_url}
        # print(json.dumps(result))
        # json_string = json.dumps(result)

        # return True, json.loads(json_string)

        reviews_for_sentiment = []
        # get reviews as list
        reviews_list = await amazon_reviews(reviews_url,reviews_for_sentiment)

        get_sentiment_details = get_sentiment(reviews_list)

        # merging 2 dicts ( result + get_sentiment_details )
        result.update(get_sentiment_details)

        return result




    except Exception as e:
        print(e)
        return False



# asyncio.run(get_product_details("https://amzn.eu/d/arWl7U2"))

# asyncio.run(amazon_reviews("https://www.amazon.in/realme-Segment-Fastest-Charging-High-res/product-reviews/B0BZ466BWW/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"))

# get_product_details("https://dl.flipkart.com/s/oUWWOpuuuN")
# get_product_details("https://www.flipkart.com/hp-pavilion-ryzen-5-hexa-core-5625u-16-gb-512-gb-ssd-windows-11-home-14-ec1005au-thin-light-laptop/p/itmec3d94a599fc0?pid=COMGHQ3NWPPAPYF4&lid=LSTCOMGHQ3NWPPAPYF4UDJA9S&marketplace=FLIPKART&store=6bo%2Fb5g&srno=b_1_1&otracker=hp_omu_Best%2Bof%2BElectronics_1_3.dealCard.OMU_96TCV7E0HFS8_3&otracker1=hp_omu_PINNED_neo%2Fmerchandising_Best%2Bof%2BElectronics_NA_dealCard_cc_1_NA_view-all_3&fm=neo%2Fmerchandising&iid=en_RaRFpSL%2FU6SQ36Om4Z8qUc2y0gOTz1g9t4HrvPij6S7yxwMOj32mirAH8jVkuBXxj0qjqb6sK%2BExAdnx%2FGvkmQ%3D%3D&ppt=dynamic&ppn=LOYALTY_PAGE&ssid=dtwj5pzj3k0000001683098252171")