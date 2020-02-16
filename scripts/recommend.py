import recent_spending
import argparse
from datetime import date

WEEKS_PER_YEAR=52
MONTHS_PER_YEAR=12
DAYS_IN_WEEK=7
DAYS_IN_MONTH=30
NUM_SUGGESTIONS=3

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
print(percent_increases)
counter = 0
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
        print("You've spent {}% more than your average on {} this {}{}".format(v,k,period,terminal))
    counter+=1