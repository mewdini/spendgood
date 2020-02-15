#/usr/bin/python3

import json
import requests

user_account = "5e481a2cf1bac107157e0abd"
key = "cb456762a68ec02541768d65d2cfa5e3"

# get purchases
def top_spending():
    url = 'http://api.reimaginebanking.com/accounts/{}/purchases?key={}'.format(user_account, key)
    purchases = requests.get(url)
    purchases_data = purchases.json()

    totals = {}
    for purchase in purchases_data:
        if "merchant_id" in purchase:
            merchant_id = purchase["merchant_id"]
            url = 'http://api.reimaginebanking.com/merchants/{}?key=cb456762a68ec02541768d65d2cfa5e3'.format(merchant_id)
            merchant = requests.get(url) #get category
            merchant_data = merchant.json()
            for category in merchant_data["category"]:
                if category in totals:
                    totals[category] += float(purchase["amount"])
                else:
                    totals[category] = float(purchase["amount"])
    totals = {k: v for k, v in sorted(totals.items(), key=lambda item: item[1], reverse=True)}
    return totals
