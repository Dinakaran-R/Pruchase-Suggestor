import asyncio
import re
import threading
import pymongo

from .amazon import get_amazon_details, amazon_reviews
from .flipkart import get_flipkart_details, flipkart_reviews
from .snapdeal import get_snapdeal_details
from .myntra import get_myntra_details
from .db import manage_products, manage_users
from .utility import isUrl, append_file, delete_file, get_current_date, id_generator
from .config import SUPPORTED_MERCHANTS

def call_after(func, arg, sec):
    def func_wrapper():
        asyncio.run(func(arg))

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

async def get_product_details(url, merchant):
    if merchant == "amazon" or merchant == "amzn":
        product_details = await get_amazon_details(url)
        # if product_details:
        #     call_after(amazon_reviews, product_details["reviewsUrl"], 60)

    elif merchant == "flipkart":
        product_details = await get_flipkart_details(url)
        # call_after(flipkart_reviews, product_details["reviewsUrl"], 60)

    elif merchant == "snapdeal":
        product_details = await get_snapdeal_details(url)

    elif merchant == "myntra":
        product_details = await get_myntra_details(url)

    return product_details

async def process_url(url):

    if not isUrl(url):
        print("Enter a Valid Url")
        return

    merchant = url.replace("www.","").split("//")[1].split(".")[0]
    print(merchant)

    product = await manage_products({"link" : url}, merchant, "read");
    print("Result: ", product)

    if not product:
        print("Not available in DB")

    details = await get_product_details(url, merchant)

    return details
    # print(data)

    # Avoid Below code. It is under construction

    # if not details:
    #     current_date = get_current_date()
    #     tracking_id = await id_generator()
    #
    #     product_details = {
    #                         "link" : details["link"], "title" : details["title"], "image" : details["image"],
    #                         "previousPrice" : details["price"], "currentPrice" : details["price"],
    #                         "lowestPrice" : details["price"], "highestPrice" : details["price"],
    #                         "startDate" : current_date, "currentDate" : current_date,
    #                         "userId": "admin", "trackingId" : "Nothing"
    #                         }
    #
    #     await manage_products(product_details, merchant , "update")
    # else:
    #     return False


async def get_tracking_list():
    # db = await connect_db()
    # collections = db.list_collection_names()
    # print(collections)
    try:
        for merchant in SUPPORTED_MERCHANTS:
            print(merchant)
            products = await manage_products({}, merchant , "read");

            i = 1
            message = ""
            for product in products:
                title = product["title"]
                price_range = product["priceRange"]
                link = product["link"]
                message += "%d. %s \n%s \n"%(i, title, link)
                i += 1
            message = "%s\n\n"%merchant + message
            append_file("Products List.txt", message)

            return message

    except Exception as e:
        print(e)
        return False


async def get_stats():
    try:
        users = await manage_users({}, "read");
        # print(users)
        total_users = len(list(users))
        message = "Total Users: %d\n"%total_users
        total_products = 0
        products_by_users = 0
        for merchant in SUPPORTED_MERCHANTS:
            products = await manage_products({}, merchant, "read");
            message += "%s Products: %d\n"%(merchant, len(list(products)))
            total_products += len(list(products))

            for product in products:
                products_by_users += len(list(product["users"]))

        message += "Total Products by Users: %d"%products_by_users

        append_file("Products List.txt", message)

        return message
    except Exception as e:
        print(e)
        return False


async def track(merchant):
    try:
        products = await manage_products({}, merchant, "read");

        list_products = list(products)
        total_products = len(list_products)
        # print(type(products))
        # test = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]

        tracked = 0
        untracked = 0
        new_prices = 0
        big_change = 0
        count = 0

        for i in range(0, total_products, 1):
            divide_products = list_products[i:i+1]
            # print(type(divide_products))
            for product in divide_products:
                # print(type(product))
                try:
                    link = product["link"]
                    details = await get_product_details(link, merchant)

                    # To details is true or not

                    price_range = product["priceRange"]
                    p_price = previous_price = price_range["currentPrice"]
                    l_price = lowest_price = price_range["lowestPrice"]
                    h_price = highest_price = price_range["highestPrice"]

                    if details:
                        tracked += 1

                        c_price = current_price = details["price"]

                        if type(previous_price) == str:
                            c_price = float(re.sub("[^0-9^.]", "",current_price))
                            p_price = float(re.sub("[^0-9^.]", "",previous_price))
                            l_price = float(re.sub("[^0-9^.]", "", lowest_price))
                            h_price = float(re.sub("[^0-9^.]", "", highest_price))

                        if c_price != p_price:
                            new_prices +=1

                            if c_price < l_price:
                                lowest_price = current_price
                            elif c_price > h_price:
                                highest_price = current_price

                            if product.get("startDate") == None:
                                start_date = get_current_date()
                            else:
                                start_date = product["startDate"]

                            if product.get("users") == None:
                                users = []
                            else:
                                users = product["users"]

                            new_values = {"link" : product["link"], "title" : details["title"], "image" : details["image"],
                                          "previousPrice" : previous_price, "currentPrice" : current_price,
                                          "lowestPrice" : lowest_price, "highestPrice" : highest_price,
                                          "startDate" : start_date , "currentDate" : get_current_date(),
                                          "users": users}

                            change = "Increased" if current_price > previous_price else "Descreased"

                            message = "The Price has been %s"%(change) + "\n\n %s"%(details["title"]) + \
                                      "\n\nPrevious Price: %s \nCurrent Price: %s"%(previous_price, current_price)


                            await manage_products(new_values, merchant, "update2")

                        # Consider Doller
                    else:
                        untracked += 1
                        c_price = -1
                    count += 1
                    msg = str(count) + " . " + product["link"] + "\nPrevious Price: "+ str(previous_price) \
                          +  "\nCurrent Price: " + str(current_price) + "\n\n"

                    append_file("TrackingList.txt", msg)
                except Exception as e:
                    print(e)


        stats = merchant + " Products: %d\n"%total_products \
                + "Tracked: %d\n"%tracked \
                + "Untracked: %d\n"%untracked \
                + "New Prices: %d\n"%new_prices \
                + "Big Change: \n\n"

        append_file("TrackingList.txt", stats)

    except Exception as e:
        print(e)
        return False


async def track_products():
    delete_file("TrackingList.txt")
    for merchant in SUPPORTED_MERCHANTS:
        await track(merchant)

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        asyncio.run(func())
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

reviews_url1 = "https://www.amazon.in/Apple-iPhone-Pro-256GB-Gold/product-reviews/B0BDK63WMS/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
reviews_url2 = "https://www.flipkart.com/samsung-galaxy-f23-5g-aqua-blue-128-gb/product-reviews/itm89d3030e3857e?pid=MOBGBKQFHKZHTHKJ&lid=LSTMOBGBKQFHKZHTHKJ7WW16A&marketplace=FLIPKART"
# call_after(flipkart_reviews, reviews_url2, 1)



# set_interval(track_products, 60)
# asyncio.run(track("amazon"))

url = "https://www.flipkart.com/samsung-galaxy-f23-5g-aqua-blue-128-gb/p/itm89d3030e3857e?pid=MOBGBKQFHKZHTHKJ&lid=LSTMOBGBKQFHKZHTHKJ7WW16A&marketplace=FLIPKART&store=tyy%2F4io&spotlightTagId=FkPickId_tyy%2F4io&srno=b_1_4&otracker=hp_omu_Top%2BOffers_1_4.dealCard.OMU_TOO4ENUDCC8Q_4&otracker1=hp_omu_PINNED_neo%2Fmerchandising_Top%2BOffers_NA_dealCard_cc_1_NA_view-all_4&fm=neo%2Fmerchandising&iid=90156599-c02b-4729-9d06-9a95b95458a1.MOBGBKQFHKZHTHKJ.SEARCH&ppt=browse&ppn=browse"

url2 = "https://www.snapdeal.com/product/aqua-grand-15-ltr-ro/626708147604#bcrumbLabelId:3631"

url3 = "https://www.myntra.com/kitchen-storage/milton/milton-pro-lunch-5pcs-black-tiffin--insulated-fabric-jacket-100ml-180ml-320ml-450ml-750ml/21779088/buy"

url4 = "https://www.myntra.com/s/buy"

url5 = "https://www.amazon.in/Redmi-Storage-Performance-Mediatek-Display/dp/B0BYN48MQW/ref=pd_day0fbt_sccl_1/260-9624651-5894348?pd_rd_w=2WfBL&content-id=amzn1.sym.9fcd4617-323e-42b7-9728-3395e1b2fea0&pf_rd_p=9fcd4617-323e-42b7-9728-3395e1b2fea0&pf_rd_r=RVFHA2XJ97RRKKNBDNQ7&pd_rd_wg=Ar5UH&pd_rd_r=9a31a763-4b1d-4aee-900d-8bd46bc1931c&pd_rd_i=B0BYN48MQW&psc=1"

# asyncio.run(process_url(url5))
