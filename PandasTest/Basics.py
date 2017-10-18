'''
Created on Oct 16, 2017

@author: ruanbo
'''

import pandas as pd
import numpy as np
from numpy import real
from tensorflow.python.ops.gen_state_ops import assign

def test1():
    s = pd.Series(np.random.randn(4), name="daily returns")
    print(s)


def multi_index():
    pd.set_option('display.max_columns', 10)
    
    pd.options.display.float_format = '{:,.2f}'.format
    
    realwage = pd.read_csv("realwage.csv")
    #print(realwage.head())
    
    #print("=============================================")

    realwage = realwage.pivot_table(values='value', index='Time',
                                    columns=['Country', 'Series', 'Pay period'])
    #print(realwage.head())
    realwage.to_csv("wage2.csv")
    
    realwage.index = pd.to_datetime(realwage.index)
    
    #print("=============================================")
    #print(type(realwage.columns))

    #print("=============================================")
    #print(realwage["Australia"].head())
    
    lowestMultiindexColumnToRowIndex = realwage.stack()
    lowestMultiindexColumnToRowIndex.to_csv("wage3.csv")
    #print("=============================================")
    #print(lowestMultiindexColumnToRowIndex.head())

    # assign the level from the multiindex column to raw index
    assignedMultiindexToRawIndex = realwage.stack(level='Country')
    assignedMultiindexToRawIndex.to_csv("wage4.csv")
    #print("=============================================")
    #print(assignedMultiindexToRawIndex.head())
    
    realwage_f = realwage.xs(('Hourly', 'In 2015 constant prices at 2015 USD exchange rates'),
                             level=('Pay period', 'Series'), axis=1)
    realwage_f.to_csv("realwage_f.csv")
    #print(realwage_f)
    
    return realwage_f


def merge_data():
    realwage_f = multi_index()
    
    worlddata = pd.read_csv("countries.csv", sep=';')
    #worlddata.to_csv("wd2.csv")
#     print(worlddata)
    
    wd = worlddata[['Country (en)', 'Continent']]
    wd = wd.rename(columns={'Country (en)':'Country'})
#     print(wd)
    
    merged = pd.merge(realwage_f.transpose(), wd, 
                      how='left', left_index=True, right_on='Country')
#     merged.to_csv("merged.csv")
#     print(merged.head())

#     print(merged[merged['Continent'].isnull()])
    
    missing_continents = {"Korea":"Asis",
                          "Russian Federation":"Europe",
                          "Slovak Republic":"Europe"}
    
    merged['Continent'] = merged['Continent'].fillna(merged['Country'].map(missing_continents))
    
#     print(merged[merged['Continent'].isnull()])

    #print(merged)
    #print("-===================================")w
    
    merged = merged.set_index(['Continent', 'Country']).sort_index()
    #print(merged)
    #print("-===================================")
    
    merged.columns = pd.to_datetime(merged.columns)
    merged.columns = merged.columns.rename("Time")
    
    #print(merged.columns)
    #print("-====================================")
    
    merged = merged.transpose()
    print(merged.head())
    

if __name__ == '__main__':
#     test1()

#     multi_index()

    merge_data()
    
    pass









