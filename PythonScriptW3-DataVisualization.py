# -*- coding: utf-8 -*-
"""
Created on Tue May 17 20:53:48 2016

@author: Chris
"""
import pandas
import numpy

#bug fix for display formats to avoid run time errors
pandas.set_option('display.float_format', lambda x:'%f'%x)

#data here will act as the data frame containing the Mars crater data
data = pandas.read_csv('marscrater_pds.csv', low_memory=False)

#convert the latitude and diameter columns so that data is display as numeric
data['LATITUDE_CIRCLE_IMAGE'] = data['LATITUDE_CIRCLE_IMAGE'].convert_objects(convert_numeric=True)
data['DIAM_CIRCLE_IMAGE'] = data['DIAM_CIRCLE_IMAGE'].convert_objects(convert_numeric=True)

#debug print code for looking at the dimensions of the data
print(len(data))
print(len(data.columns))

#record the total number of observations performed for normalizing data later'
#totalobservations = len(data)'

#bin latitude and diameter data for Mars crater

data['LATITUDE_BIN'] = pandas.cut(data['LATITUDE_CIRCLE_IMAGE'],4)
data['LATITUDE_BIN_QUARTILES'] = pandas.qcut(data['LATITUDE_CIRCLE_IMAGE'],4)
data['DIAM_BIN'] = pandas.cut(data['DIAM_CIRCLE_IMAGE'],4)
data['DIAM_BIN_QUARTILES'] = pandas.qcut(data['DIAM_CIRCLE_IMAGE'],4)

#replace data in the Ejecta morphology column that are blank with NaN
data['MORPHOLOGY_EJECTA_1'] = data['MORPHOLOGY_EJECTA_1'].replace(' ', numpy.NaN)

#create a new data table with all nan values filtered out
print('This data table shows only the craters in which there is an ejecta morpology attributed to it (level 1).')
data2 = data.dropna(subset=['MORPHOLOGY_EJECTA_1'])

#this equation was built to give you the count and percent breakdown of your observations given your bins defined
#this equation assumes your data has been cleaned because it will assume the total observations is the number of
#rows in the dataframe you provided 
def givecountandpercent(dataframe,columnname):
    totalobservations = len(dataframe)
    tempframe = pandas.DataFrame({'COUNT': dataframe.groupby(columnname).size()})
    tempframe['PERCENTAGE'] = tempframe['COUNT'].astype(float).apply(lambda x: x * 100 / totalobservations)
    tempframe.index.name = columnname
    return tempframe

print('This data table shows the count and percent of craters by latitude when grouped into 4 evenly spaced groups.')
c1 = givecountandpercent(data,'LATITUDE_BIN')
print(c1)

print('This data table shows the count and percent of craters by latitude when grouped into 4 quartiles.')
c1q = givecountandpercent(data,'LATITUDE_BIN_QUARTILES')
print(c1q)

print('This data table shows the count and percent of craters by diameter when grouped into 4 evenly spaced groups.')
c2 = givecountandpercent(data,'DIAM_BIN')
print(c2)

print('This data table shows the count and percent of craters by diameter when grouped into 4 quartiles.')
c2q = givecountandpercent(data, 'DIAM_BIN_QUARTILES')
print(c2q)

print('This data table shows the count and percentof craters by ejecta type.')
c3 = givecountandpercent(data2, 'MORPHOLOGY_EJECTA_1')
c3.sort(columns='COUNT')
print(c3)

print('This is to filter out craters with rare morphologies. This is so we can focus on the most commonly occuring \
ejecta morphology. The percentsum variable is used to calculate the cumulative sum of the percentage given \
our threshold limit. When we filter out those craters with ejecta morphologies that appear less than or equal to 10, \
we still see ~99.5% of the data.')

testcount = 10

c3revised = c3[(c3['COUNT'] > testcount)]
percentsum = c3[(c3['COUNT'] <= testcount)].sum(axis=0)