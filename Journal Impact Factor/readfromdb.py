# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 17:42:34 2021

@author: markj
"""
import os
from sqlalchemy import create_engine 
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

cwd = os.getcwd()

# Create the db engine using create_engine() method
engine = create_engine('sqlite:///' + cwd + '\\impactfactor.db')

# JIF = pd.read_sql_query('SELECT * FROM InCites', engine, index_col='index')
# PM = pd.read_sql_query('SELECT * FROM PubMed', engine, index_col='index')
# Scop= pd.read_sql_query('SELECT * FROM Scopus', engine, index_col='index')
# JIF["Journal_Title"]= JIF["Journal_Title"].str.lower()
# PM["Journal Title"]= PM["Journal Title"].str.lower()

# JIF_PM_JOIN = JIF.merge(PM, left_on = 'Journal_Title', right_on = 'Journal Title', how = 'inner')

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

#set seaborn style and context. I think darkgrid looks good for digital media

sns.set_style("darkgrid")
sns.set_context("paper")

# Create a pairplot of the 3 different 
kplot = sns.pairplot(kaggle2015[["CiteScore","SNIP","SJR"]], kind = "reg", diag_kind="kde",plot_kws={'line_kws':{'color':'red'}})
kplot.map_lower(sns.kdeplot, levels=4, color=".2")
kplot.fig.suptitle("Pairplot of CiteScore, SNIP, and SJR for 2019", y = 1.05)

kplot.savefig('2019_metric_comparison.png')
plt.show()

