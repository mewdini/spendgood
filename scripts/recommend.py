import recent_spending
import argparse
import datetime
from datetime import date
import funfacts

WEEKS_PER_YEAR=52
MONTHS_PER_YEAR=12
DAYS_IN_WEEK=7
DAYS_IN_MONTH=30
NUM_SUGGESTIONS=3
ITEM_CSV_PATH='../data/items.csv'

parser = argparse.ArgumentParser(description='Recommend how to lower spending')
parser.add_argument('--weekly', type=bool, default=False,
                    help='analyze by week (default: analyze by month)')
args = parser.parse_args()
all_totals = recent_spending.get_totals()
totals =all_totals[0]
divide_by=MONTHS_PER_YEAR
period = 'month'
offset = DAYS_IN_MONTH
if args.weekly:
    divide_by=WEEKS_PER_YEAR
    totals=all_totals[1]
    period = 'week'
    offset = DAYS_IN_WEEK
#totals: {category:[total_in_period,total_before_period, first_purchase_date]}
today = date.today()
percent_increases={}
for k,v in totals.items():
    num_days = (today - v[2]).days-offset
    average_per_day_past = 0
    if(num_days > 0):
        average_per_day_past = v[1]/num_days
    if args.weekly:
        average_per_period_past = average_per_day_past*DAYS_IN_WEEK
    else:
        average_per_period_past = average_per_day_past*DAYS_IN_MONTH
    if(average_per_period_past == 0):
        percent_increase = float('inf')
    else:
        percent_increase = 100*(v[0]/average_per_period_past-1)
    percent_increases[k]=percent_increase

percent_increases = {k: v for k, v in sorted(percent_increases.items(), key=lambda item: item[1], reverse=True)}
#print(percent_increases)
counter = 0
top = False
for k, v in percent_increases.items():
    if(counter>=NUM_SUGGESTIONS):
        break
    if(v<0):
        break
    terminal = '.'
    if(v>10):
        terminal = '!'
    if(v == float('inf')):
        print("You started spending on {} for the first time this {}!".format(k,period)) 
    else:
        #print("You've spent {:.2f}% more than your average on {} this {}{}".format(v,k,period,terminal))
        print("You've spent ${:.2f} on {} this {}. That's {:.2f}% more than your average{}".format(totals[k][0],k,period,v,terminal))
    if(counter == 0):
        top = [k,v]
    counter+=1
if(top):
    if(top[1]<float('infty')):
        recommended_percent_decrease=100*top[1]/2/(100+top[1])
    else:
        recommended_percent_decrease=50
    savings = totals[top[0]][0]*(recommended_percent_decrease)/100
    print("If you reduce your spending on {} by {:.2f}%, you could save ${:.2f} each {}{}".format(top[0],recommended_percent_decrease,savings,period,terminal))
    funfacts.have_fun(savings, ITEM_CSV_PATH)
    implement = input("Would you like to implement this into your plan?\n")
    if(implement):
        print("Budget for {} next {} ({} to {}): ${:.2f}".format(today.ToString(),(today+datetime.timedelta(days=offset)).ToString(),top[0],period,totals[top[0]][0]*(100-recommended_percent_decrease)/100))
