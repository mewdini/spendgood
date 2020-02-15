import numpy as np
import pandas as pd
import requests
import json

US_ADULT_POPULATION_2017=251564106
RCP_SCALE = 1000
customerId = '5e47858a322fa016762f38ec'
apiKey = 'e505195e938067f8af2c632e14b59140'
fpath = '../data/ECNBASIC2017.EC1744BASIC_data_with_overlays_2020-02-15T140430.csv'

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
                    category = category.lower()#.encode('ascii','ignore')
                    # if category == 'porn':
                    #     print(merchant)
                    if category not in categories:
                        categories.append(category)
                    #category = category[1:2]
                    
            else:
                merchant_category = merchant_category.lower()#.encode('ascii','ignore')
                # if merchant_category == 'porn':
                #     print(merchant)
                if merchant_category not in categories:
                        categories.append(merchant_category)

            # if i < 100:
            #     print(type(merchant["category"]))
            # i+=1

    print(categories)
else:
    print('An error has occurred.')
with open(fpath, 'r') as f:
    df = pd.read_csv(f)
    #print(df['NAICS2017_LABEL'].head)]
    census_labels = {}
    for index, row in df[['NAICS2017','NAICS2017_LABEL','RCPTOT']][2:].iterrows():
        if row['NAICS2017_LABEL'] not in census_labels:
            census_labels[row['NAICS2017_LABEL']]=float(row['RCPTOT'])*RCP_SCALE/US_ADULT_POPULATION_2017
    #for entry in df[2:]:
        #print(entry)
        # if entry['NAICS2017_LABEL'] not in census_labels:
        #     census_labels[entry['NAICS2017_LABEL']]=entry['NAICS2017']
    print(census_labels)