#/usr/bin/python3

import json
import requests
from datetime import date

user_account = "5e481a2cf1bac107157e0abd"
key = "cb456762a68ec02541768d65d2cfa5e3"

# get purchases
def recent_spending():
    url = 'http://api.reimaginebanking.com/accounts/{}/purchases?key={}'.format(user_account, key)
    purchases = requests.get(url)
    purchases_data = purchases.json()
    today = date.today()
    totals = {} #totals[category] = [this_week, before_this_week, this_month, before_this_month, first_purchase_date]
    for purchase in purchases_data:
        if "merchant_id" in purchase:
            if "purchase_date" in purchase:
                purchase_date_list=purchase["purchase_date"].split("-")
                purchase_date = date(int(purchase_date_list[0]),int(purchase_date_list[1]),int(purchase_date_list[2]))

            merchant_id = purchase["merchant_id"]
            url = 'http://api.reimaginebanking.com/merchants/{}?key={}'.format(merchant_id,key)
            merchant = requests.get(url) #get category
            merchant_data = merchant.json()
            for category in merchant_data["category"]:
                days_ago = (today - purchase_date).days
                if days_ago<7:
                    if category in totals:
                        totals[category][0] += float(purchase["amount"])
                        totals[category][2] += float(purchase["amount"])
                    else:
                        totals[category] = [float(purchase["amount"]),0,float(purchase["amount"]),0, purchase_date]
                elif days_ago<30:
                    if category in totals:
                        totals[category][1] += float(purchase["amount"])
                        totals[category][2] += float(purchase["amount"])
                    else:
                        totals[category] = [0,float(purchase["amount"]),float(purchase["amount"]),0,purchase_date]
                else:
                    if category in totals:
                        totals[category][1] += float(purchase["amount"])
                        totals[category][3] += float(purchase["amount"])
                    else:
                        totals[category] = [0,float(purchase["amount"]),0,float(purchase["amount"]),purchase_date]
                if purchase_date < totals[category][4]:
                    totals[category][4] = purchase_date
                
    totals_week = {k: v for k, v in sorted(totals.items(), key=lambda item: item[1][0], reverse=True)}
    totals_month = {k: v for k, v in sorted(totals.items(), key=lambda item: item[1][2], reverse=True)}
    return [totals_week, totals_month]
if __name__ == "__main__":
    spend_totals = recent_spending()
    print(spend_totals[0])
    print(spend_totals[1])