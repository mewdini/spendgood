import sys
import random
import pandas as pd
#USAGE: python spendgood.py SAVINGS FILEPATH
with open(sys.argv[2]) as f:
    df = pd.read_csv(f)
    saved = sys.argv[1]
    rowData = df.loc[ random.randint(0,11) , : ]
    #rowData[1] = rowData[1].strip()
    # print(rowData[1])
    # print(float(saved))
    # print(float(rowData[1][1:]))
    # print(float(saved)/float(rowData[1][1:]))
    # print('With the ${} you saved, you could have bought {} {}!'.format(saved,round((float(saved)/float(rowData[1][1:])),2),rowData['ITEM']))
    nearest_int = int((float(saved)/float(rowData[2])))
    if(nearest_int==1):
        print('With the ${:.2f} you saved, you could have bought {} {}!'.format(float(saved),nearest_int,rowData['SINGULAR']))
    else:
        print('With the ${:.2f} you saved, you could have bought {} {}!'.format(float(saved),nearest_int,rowData['ITEM']))
    if(nearest_int==69):
        print("nice")