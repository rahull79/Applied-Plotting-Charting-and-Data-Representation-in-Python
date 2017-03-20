
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/ce42cf126a5274f0a3aa1ee140ddcf82d5288d4a3ac707fa49f0eb86.csv`. The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **New Bedford, Massachusetts, United States**, and the stations the data comes from are shown on the map below.

# In[127]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import numpy as np


def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'ce42cf126a5274f0a3aa1ee140ddcf82d5288d4a3ac707fa49f0eb86')


# In[128]:

# Data for New Bedford, Massachusetts

df = pd.read_csv("data/C2A2_data/BinnedCsvs_d400/ce42cf126a5274f0a3aa1ee140ddcf82d5288d4a3ac707fa49f0eb86.csv")
df.head() 


# In[129]:

df1 = df.copy()
df1.head()


# In[131]:

df1 = df1.sort(["ID", "Date"])
df1.head(10)
#data is from 2006 to 2015
#line plot for the year 2005-2014
#scatter for 2015


# In[132]:

len(df1)


# In[133]:

#putting date into two columns by unpacking
df1['Year'], df1['Month-Day'] = zip(*df1['Date'].apply(lambda x: (x[:4], x[5:])))
df1.head()


# In[134]:

#Removing the rows which contains 2-29
df1 = df1[df1['Month-Day'] != '02-29']
df1.head()


# In[135]:

tmin  = df1[(df1['Element'] == 'TMIN') & (df1['Year'] != '2015')].groupby('Month-Day').aggregate({'Data_Value':np.min})
tmin.reset_index().head()          #365 rows


# In[136]:

tmax = df1[(df1['Element'] == 'TMAX') & (df1['Year'] != '2015')].groupby('Month-Day').aggregate({'Data_Value':np.max})
tmax.reset_index().head()


# ## Manipulating data for the year 2015

# In[137]:

min_2015 = df1[(df1['Element'] == 'TMIN') & (df1['Year'] == '2015')].groupby('Month-Day').aggregate({'Data_Value':np.min})
min_2015.reset_index().head()       #365 rows


# In[138]:

max_2015 = df1[(df1['Element'] == 'TMAX') & (df1['Year'] == '2015')].groupby('Month-Day').aggregate({'Data_Value':np.max})
max_2015.reset_index().head()


# In[139]:

a = np.where(min_2015['Data_Value'] < tmin['Data_Value'])[0]
a
#len(a) -49


# In[140]:

b = np.where(max_2015['Data_Value'] > tmax['Data_Value'])[0]
b
#len(b) -33


# In[141]:

plt.figure()

#ADDING SCATTER PLOT
plt.scatter(a, min_2015.iloc[a], s = 30, c = 'black', label = 'broken low')
plt.scatter(b, max_2015.iloc[b], s = 30, c = 'blue', label = 'broken high')

#ADDING LINE PLOT
plt.plot(tmin.values, 'g')
plt.plot(tmax.values, 'r')

plt.xlabel('Day')
plt.ylabel('Temperature in Degree Celsius')
plt.title("New Bedford Weather Plot")
plt.legend(['Min Temp', 'Max Temp', "Record Low", "Record High"], frameon = False) #loc = "center")

#Filling the required area
plt.gca().fill_between(range(len(tmax)),          #or len(tmin)
                       tmin['Data_Value'], 
                       tmax['Data_Value'], 
                       facecolor = "blue",
                       alpha = 0.2)

#Labelling ticks
plt.xticks(range(0, len(tmin), 20), tmin.index[range(0, len(tmin), 20)], rotation = '45')

#Removing the frame
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

plt.show()


# In[ ]:






