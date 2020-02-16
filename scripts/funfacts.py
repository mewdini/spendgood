import sys
import random
import pandas as pd
#USAGE: python funfacts.py SAVINGS FILEPATH
def have_fun(saved, fpath):
    with open(fpath) as f:
        df = pd.read_csv(f)
        rowData = df.loc[ random.randint(0,11) , : ]
        nearest_int = int((float(saved)/float(rowData[2])))
        if(nearest_int==1):
            print('With the ${:.2f} you\'d save, you could buy {} {}!'.format(float(saved),nearest_int,rowData['SINGULAR']))
        else:
            print('With the ${:.2f} you\'d save, you could buy {} {}!'.format(float(saved),nearest_int,rowData['ITEM']))
        if(nearest_int==69):
            print("nice")