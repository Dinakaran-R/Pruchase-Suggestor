import pymongo
import asyncio
import time

from datetime import date


myclient = pymongo.MongoClient("mongodb://localhost:27017/")

try:
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["TestBefore"]
    print("DB Connection Successful!")

except Exception as e:
    print("Failed to Connect")


async def manage_users(action, data):

    users = mydb["users"]

    try:
        if action == "read":
            result = await users.find(data)
            return True, result

        elif action == "update":
            # newvalues = {"$set": {"earnkarolink": earnkaro_link}}
            result = users.update_one({"_id":data["id"]}, {"$set": data}, upsert=True)
            return True

        elif action == "delete":
            return False

        else:
            return False

    except Exception as e:
        print(e)

async def manage_products(action, data):

    merchant = data["merchant"]
    products = mydb[merchant]

    try:
        if action == "read":
            result = await products.find(data)
            return True, result

        elif action == "update":

            # newvalues = {"$set": {"earnkarolink": earnkaro_link}}
            # newvalues = {"$push": {"pricehistory": {"Date": date, "Price": ""}}}

            price = data["price"]
            today = date.today()
            current_date = today.strftime("%d/%m/%Y")
            new_values = {"link" : data["link"], "title" : data["title"],
                        "image" : data["image"],
                        "priceRange.currentPrice" : price,
                        "priceRange.lowestPrice" : price, "priceRange.highestPrice" : price,
                        "priceRange.startDate" : current_date}


            result = products.update_one({"link":data["link"]},
                                         {"$set": new_values,
                                          "$push" : {"priceHistory": {"date" : current_date, "price" : price}}},
                                         upsert=True)
            return True

        elif action == "delete":
            return False

        else:
            return False

    except Exception as e:
        print(e)

# asyncio.run(products("update", {"id": "1", "merchant":"amazon"}))
# asyncio.run(products("update", {"id": "1", "merchant":"flipkart"}))
