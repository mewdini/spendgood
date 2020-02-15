#/usr/bin/python3

import json
import requests

user_id = "5e47855f322fa016762f38e3"
user_account = "5e481a2cf1bac107157e0abd"

key = 'cb456762a68ec02541768d65d2cfa5e3'
url = 'http://api.reimaginebanking.com/merchants?key={}'.format(key)
response = requests.get(
    url
)

ids = []
merchant_data = response.json()
for merchant in merchant_data:
    if "category" in merchant:
        for category in merchant["category"]:
            if category == "cafe":
                ids.append(merchant["_id"])

for id in ids:
    url = "http://api.reimaginebanking.com/merchants/{}/accounts/{}/purchases?key={}".format(id, user_account, key)
    response = requests.get(
        url
    )
    


average = 3.16 #hardcoded average

