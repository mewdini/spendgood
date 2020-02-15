#/usr/bin/python3

import json
import requests

user_id = "5e47855f322fa016762f38e3"
user_account = "5e481a2cf1bac107157e0abd"

key = 'cb456762a68ec02541768d65d2cfa5e3'
url = 'http://api.reimaginebanking.com/merchants?key={}'.format(key)
response = requests.get(url)

ids = []
merchant_data = response.json()
for merchant in merchant_data:
    if "category" in merchant:
        for category in merchant["category"]:
            if category == "cafe":
                ids.append(merchant["_id"])

url = 'http://api.reimaginebanking.com/accounts/{}/purchases?key={}'.format(user_account, key)
response = requests.get(url)
purchases = []
purchase_data = response.json()
total = 0

for purchase in purchase_data:
    if "merchant_id" in purchase:
        if purchase["merchant_id"] in ids:
            if "amount" in purchase:
                total = total + purchase["amount"]

print(total)


'''
#get purchases user made at cafes
total = 0
for id in ids:
    url = "http://api.reimaginebanking.com/merchants/{}/accounts/{}/purchases?key={}".format(id, user_account, key)
    response = requests.get(
        url
    )
    purchase_data = response.json()
    for purchase in purchase_data:
        if "amount" in purchase:
            total = total + purchase["amount"]

print(total)
'''



average = 3.16 #hardcoded average

