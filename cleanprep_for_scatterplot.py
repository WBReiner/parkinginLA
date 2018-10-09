
# coding: utf-8


#Import packages, %matplotlib inline to see graphs within Jupyter notebook

import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
#get_ipython().run_line_magic('matplotlib', 'inline')

#Read in csv
laParkingCitations= pd.read_csv('parking-citations.csv')

#create a df to change around so that you don't have to re-load the data if you mess up
df = laParkingCitations
print(df.columns)


# In[ ]:
df["Issue time"].isnull().sum()


# go through each one
#drop row where issue time and others are NaN
dfnew = dfnew[~dfnew['Violation Description'].isnull()]
            
#'Issue time'
#'Issue Date'
#'Latitude'
#'Longitude'
#'Violation Description
           
#columns = ['Ticket number', 'Issue time', 'Issue Date', 'Latitude', 'Longitude', 'Violation Description']

#to put in prep for scatterplot sheet
#dfnew.head()
columns = ['Issue Date', 'Issue time', "Meter Id", "RP State Plate", "Plate Expiry Date",
           "VIN", "Make", "Body Style", "Color", "Agency", "Fine amount"]

dfnew = dfnew.drop(columns, axis=1)


#fix the column names
dfnew.columns = dfnew.columns.str.lower()
dfnew.columns = dfnew.columns.str.replace(' ','')

dfnew.head()

# In[ ]:

sns.set()

cmap = sns.cubehelix_palette(rot=-.2, as_cmap=True)
ax = sns.scatterplot(x="latitude", y="longitude",
                     hue="violationdescription", size="violationdescription",
                     palette="Set2", sizes=(10, 20),
                     data=df, legend=False)

