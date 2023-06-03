from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages

from .tracker.index import process_url
import asyncio

# Create your views here.


def home(request):
    if request.method == 'POST':
        url = request.POST['link']
        print(url)
        #product_data = process_url(url)

        # temp comment starts
        product_data = asyncio.run(process_url(url))
        print("##### Product Data  #######")

        print(product_data)

        print("############")

        product_title = product_data["title"]
        product_price = product_data["price"]
        price_history = "To be updated"
        product_review = "Positive Review Percenatge is "+ str(product_data["positive_percent"])+"%. It seems reviews are "+product_data["sentiment"]

        if product_data["sentiment"] == "Positive":
            suggestion = "Review are Positive. You can buy this product!!"
        elif product_data["sentiment"] == "Negative":
            suggestion = "The Postive Reviews are too low. So better not buy it"
        else:
            suggestion = "Since the Postive percentage seems not good, you better consider before buy."

        product_link = url+"?tag=dgofferzone-21"

        #product_details = [product_title, product_price, price_history, product_review, suggestion, product_link]
        product_details = {"product_title" : product_title, "product_price" : product_price, "price_history" : price_history,
                            "product_review" : product_review, "suggestion" : suggestion, "product_link": product_link}

        # temp comment ends




        # product_details = {'product_title': 'SNSQUARE Floor Mat, Doormat, Bathroom Carpet Cushion Mat Bathroom mat Water Absorbing Non Slip Floor mat Quick Drying Water for Home Diatomite Door Mat Soft Silicone Super Absorbent',
        #                    'product_price': '₹299.00',
        #                    'price_history': 'To be updated',
        #                    'product_review': 'Review are Good',
        #                    'suggestion': 'You can buy it', 'product_link': 'https://www.amazon.in/SNSQUARE-Bathroom-Absorbing-Diatomite-Absorbent/product-reviews/B0BLYT65PR/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'}
        #

        #messages.info(request,product_details)
        print(product_details)

        return render(request,'index.html',{"product_details":product_details})


    else:
        return render(request,'index.html')
