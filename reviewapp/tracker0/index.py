import asyncio
from .amazon import *
# from .flipkart import get_flipkart_details
# from .snapdeal import get_snapdeal_details
# from .myntra import get_myntra_details
from .db import *

async def process_url(url):
    merchant = url.replace("www.","").split("//")[1].split(".")[0]
    print(merchant)
    if merchant == "amazon":
        result, data = await get_product_details(url)

    # elif merchant == "flipkart":
    #     result, data = await get_flipkart_details(url)
    #
    # elif merchant == "snapdeal":
    #     result, data = await get_snapdeal_details(url)
    #
    # elif merchant == "myntra":
    #     result, data = await get_myntra_details(url)

    print("Product Data from index.py : ",data)
    #await manage_products("update", data)
    return data





# url = "https://www.flipkart.com/samsung-galaxy-f23-5g-aqua-blue-128-gb/p/itm89d3030e3857e?pid=MOBGBKQFHKZHTHKJ&lid=LSTMOBGBKQFHKZHTHKJ7WW16A&marketplace=FLIPKART&store=tyy%2F4io&spotlightTagId=FkPickId_tyy%2F4io&srno=b_1_4&otracker=hp_omu_Top%2BOffers_1_4.dealCard.OMU_TOO4ENUDCC8Q_4&otracker1=hp_omu_PINNED_neo%2Fmerchandising_Top%2BOffers_NA_dealCard_cc_1_NA_view-all_4&fm=neo%2Fmerchandising&iid=90156599-c02b-4729-9d06-9a95b95458a1.MOBGBKQFHKZHTHKJ.SEARCH&ppt=browse&ppn=browse"
#
# url2 = "https://www.snapdeal.com/product/aqua-grand-15-ltr-ro/626708147604#bcrumbLabelId:3631"
#
# url3 = "https://www.myntra.com/kitchen-storage/milton/milton-pro-lunch-5pcs-black-tiffin--insulated-fabric-jacket-100ml-180ml-320ml-450ml-750ml/21779088/buy"
# asyncio.run(process_url(url3))

# asyncio.run(processUrl("https://www.amazon.in/Redmi-Storage-Performance-Mediatek-Display/dp/B0BYN48MQW/ref=pd_day0fbt_sccl_1/260-9624651-5894348?pd_rd_w=2WfBL&content-id=amzn1.sym.9fcd4617-323e-42b7-9728-3395e1b2fea0&pf_rd_p=9fcd4617-323e-42b7-9728-3395e1b2fea0&pf_rd_r=RVFHA2XJ97RRKKNBDNQ7&pd_rd_wg=Ar5UH&pd_rd_r=9a31a763-4b1d-4aee-900d-8bd46bc1931c&pd_rd_i=B0BYN48MQW&psc=1"))
