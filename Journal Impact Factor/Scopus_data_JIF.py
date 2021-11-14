# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 10:34:48 2021

@author: markj
"""

import os
from sqlalchemy import create_engine 
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Get current working directory for create_engine()
cwd = os.getcwd()

# Set seaborn style and context. I think darkgrid looks good for digital media

sns.set_style("darkgrid")
sns.set_context("paper")
# setting dpi resolution for later figure exports
resol = 300

def pcnt(df_col,pct):
    return np.percentile(df_col,pct)
    

# Create the db engine using create_engine() method
engine = create_engine('sqlite:///' + cwd + '\\impactfactor.db')

# Load Scopus 2020 data taking only the relevant columns from impactfactor.db    
scopus= pd.read_sql_query('SELECT "Journal_Title", Publisher, "Citation_Count", Documents, CiteScore, SNIP, SJR FROM Scopus', engine)

# Remove duplicates since we aren't including all columns
scopus = scopus.drop_duplicates()

# Find the top 6 publishers by amount of documents published in 2020
scopus_grouped_publisher = scopus.groupby('Publisher').sum().sort_values('Documents', ascending = False)
top_6_publishers = scopus_grouped_publisher.reset_index()['Publisher'][0:6]

# Select only those publishers from the full list
scopus_top6 = scopus[scopus['Publisher'].isin(top_6_publishers)]

# Cat plot using Publisher as columns to show box plots of #Documents published

top_6_boxplot = sns.catplot(data = scopus_top6, y= 'Documents', kind = 'box', col = 'Publisher', col_wrap = 3)

# Use a log scale to better visualise the distribution
axes = top_6_boxplot.axes.flat
for i in axes:
        i.set_yscale('log')
        
top_6_boxplot .set_ylabels('# Documents published (log)')
top_6_boxplot.fig.suptitle("Box plot of No. Documents Published by each Journal Within the Top 5 Publishers", y = 1.05)
top_6_boxplot.savefig('Top_5_boxplot.png', dpi = resol)
plt.clf()

# Load Journal Impact Factor data taking only the relevant columns from impactfactor.db    
incites= pd.read_sql_query('SELECT "Journal_Title", "Total_Citations", JIF, ES FROM Incites', engine)

#set "Journal_Title" to lowercase to increase chance of merging on this index
scopus['Journal_Title']=scopus['Journal_Title'].str.lower()
incites['Journal_Title']=incites['Journal_Title'].str.lower()

# inner join on data to only keep matching pairs
merged_data = scopus.merge(incites, on = "Journal_Title" )
# remove outliner with JIF of >500
merged_data = merged_data[merged_data['JIF']<500]

Doc90pct = pcnt(merged_data['Documents'],90)
Doc50pct = pcnt(merged_data['Documents'],50)
JIF90pct = pcnt(merged_data['JIF'],90)

plt.figure()
Doc_vs_JIF = sns.jointplot(data = merged_data, x = 'Documents', y = 'JIF')
Doc_vs_JIF.ax_joint.axvline(x=Doc90pct, color = 'r', linestyle='--')
Doc_vs_JIF.ax_joint.axhline(y=JIF90pct, color = 'r', linestyle='--')

Doc_vs_JIF.ax_joint.set_xlabel("# Documents Published")
Doc_vs_JIF.ax_joint.set_ylabel("Journal Impact Factor")
Doc_vs_JIF.fig.suptitle("Documents Published vs Impact Factor per Journal", y=1.03)
Doc_vs_JIF.fig.text(0.6,0.18,"90th Percentile",fontdict=dict(size=10))
Doc_vs_JIF.fig.text(0.15,0.55,"90th Percentile",fontdict=dict(size=10), rotation = -90)

Doc_vs_JIF.savefig('Doc_vs_JIF.png', dpi = resol)

# Number of journals that publish more than the 90th percentile, but have JIF > than the 90th percentile
print("The number of journals that publish more than the 90th percentile, \
      but maintain an impact factor above the 90th percentile is: " 
          + str(len(merged_data[(merged_data['Documents']>Doc90pct) & (merged_data['JIF']>JIF90pct)])))
# Number of journals that publish fewer than the 90th percentile, but have JIF > than the 90th percentile
print("The number of journals that publish less than the 90th percentile, \
      ut maintain an impact factor above the 90th percentile is: "
          + str(len(merged_data[(merged_data['Documents']<Doc90pct) & (merged_data['JIF']>JIF90pct)])))