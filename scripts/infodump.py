#/usr/bin/python3

import get_yearly
import top_spending

# array[0] is string with percentage, array[1] is string with difference
def percentage(user_spending, natl_avg):
    percentage = str(user_spending/natl_avg*100)
    difference = str(user_spending-natl_avg)
    if user_spending > natl_avg:
        return ["You're spending " + percentage +"% more than the national average.", "You're spending $" + difference + " more than the national average."]
    elif user_spending < natl_avg:
        return ["You're spending " + percentage +"% less than the national average.", "You're spending $" + difference + " less than the national average"]
    else:
        return "You're spending as much as the national average."
