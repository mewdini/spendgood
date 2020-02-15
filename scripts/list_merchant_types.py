import numpy as np
import pandas as pd
import requests
import json

customerId = '5e47858a322fa016762f38ec'
apiKey = 'e505195e938067f8af2c632e14b59140'

url = 'http://api.reimaginebanking.com/enterprise/merchants?key={}'.format(apiKey)

# Create a Savings Account
response = requests.get( 
	url
	)

if response:
    print('Success!')
else:
    print('An error has occurred.')