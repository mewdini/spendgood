import numpy as np
#import pandas as pd
import requests
import json

customerId = '5e47858a322fa016762f38ec'
apiKey = 'e505195e938067f8af2c632e14b59140'

url = 'http://api.reimaginebanking.com/merchants?key={}'.format(apiKey)

# Create a Savings Account
response = requests.get( 
	url
	)
categories = []
if response:
    print('Success!')
    merchants = response.json()
    i = 0
    for merchant in merchants:
        if "category" in merchant:
            # for category in merchant["category"]:
            #     if category not in categories:
            #         categories.append(category)
            merchant_category = merchant["category"]
            if type(merchant_category) == list:
                merchant_categories = merchant_category
                for category in merchant_categories:
                    category = category.lower().encode('ascii','ignore')
                    # if category == 'rip-offs':
                    #     print(merchant)
                    if category not in categories:
                        categories.append(category)
                    #category = category[1:2]
                    
            else:
                merchant_category = merchant_category.lower().encode('ascii','ignore')
                
                if merchant_category not in categories:
                        categories.append(merchant_category)

            # if i < 100:
            #     print(type(merchant["category"]))
            # i+=1

    print(categories)
else:
    print('An error has occurred.')