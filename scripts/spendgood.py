import sys
import random
import pandas as pd
with open(sys.argv[2]) as f:
    df = pd.read_csv(f)
    saved = sys.argv[1]
    rowData = df.loc[ random.randint(0,9) , : ]
    rowData[1] = rowData[1].strip()
    # print(rowData[1])
    # print(float(saved))
    # print(float(rowData[1][1:]))
    # print(float(saved)/float(rowData[1][1:]))
    # print('With the ${} you saved, you could have bought {} {}!'.format(saved,round((float(saved)/float(rowData[1][1:])),2),rowData['ITEM']))
    print('With the ${} you saved, you could have bought {} {}!'.format(saved,int((float(saved)/float(rowData[1][1:]))),rowData['ITEM']))