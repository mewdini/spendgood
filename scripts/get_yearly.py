#/usr/bin/python3

import pandas as pd

fpath = '../data/ECNBASIC2017.EC1744BASIC_data_with_overlays_2020-02-15T140430.csv'
US_ADULT_POPULATION_2017=251564106
RCP_SCALE = 1000
def get_yearly():
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
        return(census_labels)