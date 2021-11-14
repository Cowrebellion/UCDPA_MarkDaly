# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 11:41:38 2021

@author: markj
"""

import os
from sqlalchemy import create_engine 
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Get current working directory for create_engine()
cwd = os.getcwd()

# Create the db engine using create_engine() method
engine = create_engine('sqlite:///' + cwd + '\\impactfactor.db')

# Function that returns a dataframe with the maximum CiteScore datapoint removed
def CS_Outlier(df):
    df = df[df['CiteScore']<df['CiteScore'].max()]
    return df
    

# Load last 5 years of data from Kaggle taking only the relevant columns from impactfactor.db    
kaggle2015 = pd.read_sql_query('SELECT "Source title", Publisher, Citations, Documents, CiteScore, SNIP, SJR FROM kaggledata2015', engine)
kaggle2016 = pd.read_sql_query('SELECT "Source title", Publisher, Citations, Documents, CiteScore, SNIP, SJR FROM kaggledata2016', engine)
kaggle2017 = pd.read_sql_query('SELECT "Source title", Publisher, Citations, Documents, CiteScore, SNIP, SJR FROM kaggledata2017', engine)
kaggle2018 = pd.read_sql_query('SELECT "Source title", Publisher, Citations, Documents, CiteScore, SNIP, SJR FROM kaggledata2018', engine)
kaggle2019 = pd.read_sql_query('SELECT "Source title", Publisher, Citations, Documents, CiteScore, SNIP, SJR FROM kaggledata2019', engine)

# Remove outlier from each using the fuction CS_outlier
kaggle2015 = CS_Outlier(kaggle2015)
kaggle2016 = CS_Outlier(kaggle2016)
kaggle2017 = CS_Outlier(kaggle2017)
kaggle2018 = CS_Outlier(kaggle2018)
kaggle2019 = CS_Outlier(kaggle2019)

# Set seaborn style and context. I think darkgrid looks good for digital media

sns.set_style("darkgrid")
sns.set_context("paper")

# # Create a pairplot of the 3 different journal-based metrics provided in the Kaggle data for 2019
# kplot = sns.pairplot(kaggle2015[["CiteScore","SNIP","SJR"]], kind = "reg", diag_kind="kde",plot_kws={'line_kws':{'color':'red'}})
# # Add a kdeplot to the lower plots to show the distribution of each journal based metric
# kplot.map_lower(sns.kdeplot, levels=4, color=".2")
# kplot.fig.suptitle("Pairplot of CiteScore, SNIP, and SJR for 2019", y = 1.05)

# # Save the figure to .png for including in report
# kplot.savefig('2019_metric_comparison.png')


# Next I want to see some trends over the past 5 years for the top 10 journals in 2019 as determine by CiteScore
# Inner merge as I only want to keep matching pairs
kaggle_merge = kaggle2019.merge(kaggle2018[["Source title","CiteScore", "SNIP", "SJR"]], on = 'Source title', suffixes = (None,"_2018"))
kaggle_merge = kaggle_merge.merge(kaggle2017[["Source title","CiteScore", "SNIP", "SJR"]], on = 'Source title', suffixes = (None,"_2017"))
kaggle_merge = kaggle_merge.merge(kaggle2016[["Source title","CiteScore", "SNIP", "SJR"]], on = 'Source title', suffixes = (None,"_2016"))
kaggle_merge = kaggle_merge.merge(kaggle2015[["Source title","CiteScore", "SNIP", "SJR"]], on = 'Source title', suffixes = (None,"_2015"))

# Sort by CiteScore and find the top 10 for 2019
sort_2019 = kaggle2019.sort_values('CiteScore', ascending = False)
Top_10 = sort_2019['Source title'][0:10]

# Find the entries for hte top 10 in 5 previous years. Not all entries may match 

Top_CS_merge = kaggle_merge[kaggle_merge['Source title'].isin(Top_10)]
Top_CS_merge=Top_CS_merge.rename(columns = {'CiteScore_2015':'2015','CiteScore_2016':'2016','CiteScore_2017':'2017','CiteScore_2018':'2018','CiteScore':'2019'})
Top_CS_merge.loc[Top_CS_merge['Source title']=='MMWR. Surveillance summaries : Morbidity and mortality weekly report. Surveillance summaries / CDC','Source title']='MMWR. Surveillance summaries'
  
Top_CS_merge_melt = pd.melt(Top_CS_merge, id_vars=('Source title'), value_vars=['2015','2016','2017','2018','2019'])

Top_7_plot = sns.catplot(data = Top_CS_merge_melt, y= 'value', kind = 'strip', x = 'variable', hue = 'Source title', jitter = False)

Top_7_plot.set_xticklabels(rotation = 45)
Top_7_plot.set_ylabels('CiteScore')
Top_7_plot.set_xlabels('Year')
Top_7_plot.fig.suptitle("Strip Plot of CiteScore vs Year for the Top 7 journals from 2019", y = 1.05)
Top_7_plot.savefig('Top_7_CiteScore_2015-2019.png')



