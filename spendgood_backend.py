import requests
from flask import Flask, render_template, request, redirect
import json
import requests
from datetime import date
import pandas as pd
import random
import datetime

app = Flask(__name__)

#the users id for nessie api interaction
global plan
plan = False

global user_id
user_id = ""

global username
username = ""

global user_display
user_display = ""

global password
password = ""

global plan_location
plan_location = ""

global plan_period
plan_period = ""

global plan_start
plan_start = ""

global plan_end
plan_end = ""

global plan_budget
plan_budget = ""

key = "cb456762a68ec02541768d65d2cfa5e3"

def have_fun(saved, csv_file):
    df = pd.read_csv(csv_file)
    rowData = df.loc[ random.randint(0,11) , : ]
    nearest_int = int((float(saved)/float(rowData[2])))
    return_string = ""
    if(nearest_int==1):
        return_string += 'With the ${:.2f} you\'d save, you could buy {} {}!'.format(float(saved),nearest_int,rowData['SINGULAR']) + "\n"
    else:
        return_string += 'With the ${:.2f} you\'d save, you could buy {} {}!'.format(float(saved),nearest_int,rowData['ITEM']) + "\n"
    if(nearest_int==69):
        return_string += 'nice' + "\n"

    return return_string

def get_totals():

    url = "http://api.reimaginebanking.com/accounts/" + user_id + "/purchases?key=" + key

    payload = {}
    headers= {}

    response = requests.request("GET", url, headers=headers, data = payload)

    print(response)
    purchases_data = response.json()

    today = date.today()
    totals = {} #totals[category] = [this_week, before_this_week, this_month, before_this_month, first_purchase_date]
    for purchase in purchases_data:
        if "merchant_id" in purchase:
            if "purchase_date" in purchase:
                purchase_date_list=purchase["purchase_date"].split("-")
                purchase_date = date(int(purchase_date_list[0]),int(purchase_date_list[1]),int(purchase_date_list[2]))

            merchant_id = purchase["merchant_id"]

            url = "http://api.reimaginebanking.com/merchants/" + merchant_id + "?key=" + key

            payload = {}
            headers= {}

            merchant = requests.request("GET", url, headers=headers, data = payload)

            #print(response)
            merchant_data = merchant.json()

            #if(type(merchant_data["category"])==list):
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
            '''else:
                category = merchant_data["category"]
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
                    totals[category][4] = purchase_date'''

    totals_month = {k: v for k, v in sorted(totals.items(), key=lambda item: item[1][2], reverse=True)}
    totals_month = {k: [v[2],v[3],v[4]] for k,v in totals_month.items()}
    totals_week = {k: v for k, v in sorted(totals.items(), key=lambda item: item[1][0], reverse=True)}
    totals_week = {k: [v[1],v[2],v[4]] for k,v in totals_week.items()}
    return [totals_month, totals_week]


def get_recommend():
    WEEKS_PER_YEAR=52
    MONTHS_PER_YEAR=12
    DAYS_IN_WEEK=7
    DAYS_IN_MONTH=30
    NUM_SUGGESTIONS=3
    ITEM_CSV_FILE='./items.csv'
    weekly = True #change this to true or have it change by user selection
    #parser = argparse.ArgumentParser(description='Recommend how to lower spending')
    #parser.add_argument('--weekly', type=bool, default=False,
                        #help='analyze by week (default: analyze by month)')
    #args = parser.parse_args()

    all_totals = get_totals() #import this?
    totals =all_totals[0]
    divide_by=MONTHS_PER_YEAR
    period = 'month'
    offset = DAYS_IN_MONTH

    if weekly:
        divide_by=WEEKS_PER_YEAR
        totals=all_totals[1]
        period = 'week'
        offset = DAYS_IN_WEEK

    API_to_census = {'furniture_store':'Furniture stores','Lodging':'Home centers','Tech':'Electronics and appliance stores','book_store':'Book stores','Nut Store':'Confectionery and nut stores','wholesale':'Warehouse clubs and supercenters','specialty':"All other specialty food stores",'groceries':'Grocery stores','food':'Food and beverage stores'}
    yearly_sales = get_yearly()
    today = date.today()
    percent_increases={}
    for k,v in totals.items():
        num_days = (today - v[2]).days-offset
        average_per_day_past = 0
        if(num_days > 0):
            average_per_day_past = v[1]/num_days
        if weekly:
            average_per_period_past = average_per_day_past*DAYS_IN_WEEK
        else:
            average_per_period_past = average_per_day_past*DAYS_IN_MONTH
        if(average_per_period_past == 0):
            percent_increase = float('inf')
        else:
            percent_increase = 100*(v[0]/average_per_period_past-1)
        percent_increases[k]=percent_increase

    percent_increases = {k: v for k, v in sorted(percent_increases.items(), key=lambda item: item[1], reverse=True)}
    print("PERCENT INC: ", percent_increases)
    #print(percent_increases)
    counter = 0
    top=[]
    return_string = ""
    for k, v in percent_increases.items():
        print("COUNTER", counter)
        if(counter>=NUM_SUGGESTIONS):
            break
        if(v<0):
            break
        terminal = '.'
        if(v>10):
            terminal = '!'
        if(v == float('inf')):
            return_string += "You started spending on {} for the first time this {}!".format(k,period) + "\n"
        else:
            print("K: ", k)
            #return_string += "You've spent {:.2f}% more than your average on {} this {}{}".format(v,k,period,terminal) + "\n"
            return_string += "You've spent ${:.2f} on {} this {}. That's {:.2f}% more than your average{}".format(totals[k][0],k,period,v,terminal) + "\n"
            return_string += "The average American adult spent ${:.2f} on {} each {} in 2017.".format(yearly_sales[API_to_census[k]]/divide_by,k,period) + "\n"
        if(counter == 0):
            print("KV", [k,v])
            top = [k,v]
        counter+=1

    if(top):
        if(top[1]<float('inf')):
            recommended_percent_decrease=100*top[1]/2/(100+top[1])
        else:
            recommended_percent_decrease=50
        savings = totals[top[0]][0]*(recommended_percent_decrease)/100
        return_string += "If you reduce your spending on {} by {:.2f}%, you could save ${:.2f} each {}{}".format(top[0],recommended_percent_decrease,savings,period,terminal) + "\n"
        joke_suggestion = have_fun(savings, ITEM_CSV_FILE)
        return_string += joke_suggestion
        #implement = input("Would you like to implement this into your plan?\n")
        if(not plan):
            global plan_location
            plan_location = top[0]

            global plan_period
            plan_period = period

            global plan_start
            plan_start = (today+datetime.timedelta(days=1)).strftime("%m/%d/%Y")

            global plan_end
            plan_end = (today+datetime.timedelta(days=offset+1)).strftime("%m/%d/%Y")

            global plan_budget
            plan_budget = totals[top[0]][0]*(100-recommended_percent_decrease)/100

    return return_string
#return a boolean True if there is a plan and set the plan
def is_plan():
    url = "https://vthacks2020.firebaseio.com/" + username + "/.json"

    payload = {}
    headers= {}

    response = requests.request("GET", url, headers=headers, data = payload)
    response = response.json()

    if 'plan_location' in response:
        global plan_location
        plan_location = response['plan_location']

        global plan_period
        plan_period = response['plan_period']

        global plan_start
        plan_start = response['plan_start']

        global plan_end
        plan_end = response['plan_end']

        global plan_budget
        plan_budget = response['plan_budget']

        return True
    else:
        return False


def get_yearly():
    file_name = 'ECNBASIC2017.EC1744BASIC_data_with_overlays_2020-02-15T140430.csv'
    US_ADULT_POPULATION_2017=251564106
    RCP_SCALE = 1000
    #with open(fpath, 'r') as f:
    df = pd.read_csv(file_name)
    #print(df['NAICS2017_LABEL'].head)]
    census_labels = {}
    for index, row in df[['NAICS2017','NAICS2017_LABEL','RCPTOT']][2:].iterrows():
        if row['NAICS2017_LABEL'] not in census_labels:
            census_labels[row['NAICS2017_LABEL']]=float(row['RCPTOT'])*RCP_SCALE/US_ADULT_POPULATION_2017
    #for entry in df[2:]:
        #print(entry)
        # if entry['NAICS2017_LABEL'] not in census_labels:
        #     census_labels[entry['NAICS2017_LABEL']]=entry['NAICS2017']
    return(census_labels)




#add code to change html depending on if there is a plan
@app.route('/get-spending/')
def get_spending():
    global plan
    plan = is_plan()

    html_final = """
    <!DOCTYPE html>
    <html lang=en>
      <head>
        <title>My Funds</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" type="text/css" href="//fonts.googleapis.com/css?family=Lemon" />
        <style>
        * {
            box-sizing: border-box;
        }

        /* Create two equal columns that floats next to each other */
        .column {
            float: left;
            width: 50%;
            padding: 10px;
            height: 300px; /* Should be removed. Only for demonstration */
        }

        /* Clear floats after the columns */
        .row:after {
            content: "";
            display: table;
            clear: both;
        }
        </style>
      </head>

      <body style="background-color:#1abc9c">
      """

    if plan:
        plan = "Budget for {} next {} ({} to {}): ${:.2f}".format(plan_location, plan_period, plan_start, plan_end, float(plan_budget))
        html_final += """<h1 style="text-align:center;color:#ebcbd7"><font face=Calligraphy size = 6>""" + plan + """</font></h1>"""

    html_final += """<table bgcolor="white" style="margin-left:10%;width:80%; border: solid 2px black; ">
          <tr style = "border: solid 2px black">
            <th style="border-right: dotted 1px black">Categories</th>
            <th> Amount Spent </th>
          </tr>"""

    url = "http://api.reimaginebanking.com/accounts/" + user_id + "/purchases?key=" + key

    payload = {}
    headers= {}

    response = requests.request("GET", url, headers=headers, data = payload)

    print(response)
    purchases_data = response.json()

    #need to get purchase data information
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

    for item in totals:
        html = """
        <tr>
          <td style="text-align:center; border-right: dotted 1px black">""" + item + """</td>
           <td style ="text-align:center"> """ + """$""" + str(totals[item]) + """ </td>
        </tr>"""
        html_final+= html
    html_final += """</table> <iframe width="80%" height="600" style="margin-left: 10%" src='""" + user_display + """'></iframe>"""
    recommend = get_recommend()
    recommend_list = recommend.split("\n")
    html_final += """
    <div style="width:80%;margin-left:10% ">
        <div class="row">
            <div class="column">"""
    front_data = recommend_list[:-3]
    back_data = recommend_list[-3:]
    for item in front_data:
        html_final += """<h1 style="text-align:center;color:white"><font face=Calligraphy size = 5>""" + item + """</font></h1>"""
    html_final += """
            </div>
            <div class="column" style="margin-top:50px;">"""
    for item in back_data:
        html_final += """<h1 style="text-align:center;color:white"><font face=Calligraphy size = 5>""" + item + """</font></h1>"""
    html_final += """
            </div>
        </div>
    </div>"""


    if not plan:
        print("PLAN BUDGET:", plan_budget)
        plan = "Budget for {} next {} ({} to {}): ${:.2f}".format(plan_location, plan_period, plan_start, plan_end, float(plan_budget))
        html_final += """<h1 style="text-align:center;color:white;margin-top:10%;"><font face=Calligraphy size = 5>""" + plan + """</font></h1>"""

        html_final += """<h2 style="text-align:center;color:#ebcbd7"> <font face=Calligraphy size = 5> Do you want to set this budget as your plan? </font> </h2>
        <div>
        <form style= "color:white" action="/add-plan/" method="post">
            <input style="width:20%; height:50px; margin-left:40%; margin-bottom:25px;" type="submit" value="Add to Plan"></input>
        </form>
        </div>"""

    html_final += """
    <div>
    <form style= "color:white" action="/">
        <input style="width:20%; height:50px; margin-left:40%" type="submit" value="Logout"></input>
    </form>
    </div>"""

    html_final += """</body></html>"""
    return html_final

@app.route('/add-plan/', methods = ['POST'])
def add_plan():
    #print("hello world")
    url = "https://vthacks2020.firebaseio.com/" + username + "/.json"

    payload = {}
    headers= {}

    response = requests.request("GET", url, headers=headers, data = payload)
    response = response.json()

    global user_id
    user_id = response['userID']

    global password
    password = response['password']

    global user_display
    user_display = response['display']

    url = "https://vthacks2020.firebaseio.com/" + username + "/.json"

    payload = "{\n\t\"display\": \"" + user_display + "\",\n\t\"password\": \""+ password + "\",\n\t\"userID\": \""+ user_id +"\", \n\t\"plan_location\": \""+ plan_location +"\", \n\t\"plan_period\": \""+plan_period +"\", \n\t\"plan_start\": \""+plan_start + "\", \n\t\"plan_end\": \""+ plan_end +"\", \n\t\"plan_budget\": \""+ str(plan_budget) +"\"\n\t\n}"
    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("PUT", url, headers=headers, data = payload)

    return redirect('/get-spending/')

@app.route('/')
def start():
    return render_template("home.html")

@app.route('/check-id/', methods = ['POST'])
def check_id():
    global username
    username = request.form['username']
    global password
    password = request.form['password']

    print(username, password)

    if username != "":
        url = "https://vthacks2020.firebaseio.com/" + username + "/.json"

        payload = {}
        headers= {}

        response = requests.request("GET", url, headers=headers, data = payload)

        response = response.json()
        #print(response)

        if response is not None:
            correct_pass = response['password']

            if password == correct_pass:
                #print('matched passwords', correct_pass, password)
                global user_id
                user_id = response['userID']
                global user_display
                user_display = response['display']
                #print(user_id)
                return redirect('/get-spending/')
            else:
                return redirect('/')
        else:
            return redirect('/')
    else:
        #print('did not match passwords', correct_pass, password)
        return redirect('/')


    #return redirect("testing_firebase.html")

if __name__ == '__main__':
    #main_execution.initialize_database()
    app.run(host='0.0.0.0', debug=True)



'''
when the user "logons", they see their finances (call to nessie api) and display using
microstragety

below this information, the program suggests a reccomendation on how to save money by analyzing
financial data

they can accept the suggestion or reject it, which then updates their personal goal
if they accept, their financial page gets updated with their goal
they see their spending compared to others/their past spending
the goals that they set for themselves are stored in their "account" on firebase (read: their db entry)

user can see how much of their income they spend (in a way that is shocking)
user can also see comparisons to small high quantity items (like gumballs, toilet paper, etc)
'''
