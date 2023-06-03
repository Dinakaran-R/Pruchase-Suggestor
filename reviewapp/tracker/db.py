import pymongo
import asyncio
from .config import DB_URL
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")

myclient = None

async def connect_db():
    try:
        my_client = pymongo.MongoClient(DB_URL)
        db = my_client["TestBefore"]
        print("DB Connection Successful!")
        return db

    except Exception as e:
        print("Failed to Connect" , e)
        return False


async def manage_users(data, action):
    db = await connect_db()

    try:
        users = db["users"]

        if action == "read":
            result = users.find(data)
            return result

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

async def manage_products(data, merchant, action):
    db = await connect_db()

    try:
        products = db[merchant]

        if action == "read":
            result = products.find(data)
            # print("Result ", result)
            return result

        elif action == "update" or action == "update2":

            # newvalues = {"$set": {"earnkarolink": earnkaro_link}}
            # newvalues = {"$push": {"pricehistory": {"Date": date, "Price": ""}}}

            price = data["currentPrice"]

            current_date = data["currentDate"]

            new_values = {
                        "link" : data["link"], "title" : data["title"],
                        "image" : data["image"],
                        "priceRange" : {
                            "currentPrice" : price,
                            "lowestPrice"  : data["lowestPrice"],
                            "previousPrice": data["previousPrice"],
                            "highestPrice" : data["highestPrice"],
                            "startDate" : data["startDate"]
                             }
                        }

            if action == "update2":
                new_values["users"] = data["users"]
                result = products.update_one({"link": data["link"]},
                                             {"$set": new_values,
                                              "$push": {"priceHistory": {"date": current_date, "price": price}},
                                              },
                                             upsert=True)

            else:
                result = products.update_one({"link":data["link"]},
                                         {"$set": new_values,
                                          "$push" : {"priceHistory": {"date" : current_date, "price" : price}},
                                          "$addToSet" : {"users": {"userid": data["userId"],
                                                                   "trackingId": data["trackingId"]}}},
                                         upsert=True)
            return True

        elif action == "delete":
            products.update_one({"users": data},
                                {"$pull" : data },)
            return True

        else:
            return False

    except Exception as e:
        print(e)
        return False

# asyncio.run(products("update", {"id": "1", "merchant":"amazon"}))
# asyncio.run(products("update", {"id": "1", "merchant":"flipkart"}))
