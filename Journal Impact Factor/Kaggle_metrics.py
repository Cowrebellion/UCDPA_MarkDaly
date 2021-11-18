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
from scipy import stats

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

# Remove outlier from each using the fuction CS_outlier. 
# There is one journal that consistently pulls really far ahead of all other journals and it pulls out the scale too much on graphics.
kaggle2015 = CS_Outlier(kaggle2015)
kaggle2016 = CS_Outlier(kaggle2016)
kaggle2017 = CS_Outlier(kaggle2017)
kaggle2018 = CS_Outlier(kaggle2018)
kaggle2019 = CS_Outlier(kaggle2019)

# Set seaborn style and context

sns.set_style("darkgrid")
sns.set_context("paper")



# Create a pairplot of the 3 different journal-based metrics provided in the Kaggle data for 2019
kplot = sns.pairplot(kaggle2019[["CiteScore","SNIP","SJR"]], kind = "reg", plot_kws={'line_kws':{'color':'red'}})
# Add a kdeplot to the lower plots to show the distribution of each journal based metric
kplot.map_lower(sns.kdeplot, levels=4, color=".2")
kplot.fig.suptitle("Pairplot of CiteScore, SNIP, and SJR for 2019", y = 1.05)

# Use scipy's stats.linregress function to determine the goodness of fit. seaborn can visualise the regressions, but will not print the underlying fit params.
slope, intercept, r, p, std_err = stats.linregress(kaggle2019["SNIP"], kaggle2019["CiteScore"])
slope2, intercept2, r2, p2, std_err2 = stats.linregress(kaggle2019["SJR"], kaggle2019["SNIP"])
slope3, intercept3, r3, p2, std_err3 = stats.linregress(kaggle2019["CiteScore"], kaggle2019["SJR"])

# Add R values to plots
kplot.fig.text(0.59,0.7,"R = %.3f"%r ,fontdict=dict(size=10))
kplot.fig.text(0.29,0.39,"R = %.3f"%r ,fontdict=dict(size=10))
kplot.fig.text(0.89,0.39,"R = %.3f"%r2 ,fontdict=dict(size=10))
kplot.fig.text(0.59,0.085,"R = %.3f"%r2,fontdict=dict(size=10))
kplot.fig.text(0.89,0.7,"R = %.3f"%r3,fontdict=dict(size=10))
kplot.fig.text(0.29,0.085,"R = %.3f"%r3 ,fontdict=dict(size=10))

# Save the figure to .png for including in report
kplot.savefig('Images\\2019_metric_comparison.png',dpi = 1000)

plt.clf()

print ('R value for CS vs SNIP is: ' + str(r) +'\n R value for CS vs SJR is: ' + str(r2) +'\n R value for SNIP vs SJR is: ' + str(r3))

# Next I want to see some trends over the past 5 years for the top 10 journals in 2019 as determine by CiteScore
# Inner merge as I only want to keep matching pairs
kaggle_merge = kaggle2019.merge(kaggle2018[["Source title","CiteScore", "SNIP", "SJR"]], on = 'Source title', suffixes = (None,"_2018"))
kaggle_merge = kaggle_merge.merge(kaggle2017[["Source title","CiteScore", "SNIP", "SJR"]], on = 'Source title', suffixes = (None,"_2017"))
kaggle_merge = kaggle_merge.merge(kaggle2016[["Source title","CiteScore", "SNIP", "SJR"]], on = 'Source title', suffixes = (None,"_2016"))
kaggle_merge = kaggle_merge.merge(kaggle2015[["Source title","CiteScore", "SNIP", "SJR"]], on = 'Source title', suffixes = (None,"_2015"))

# Sort by CiteScore and find the top 10 for 2019
sort_2019_CS = kaggle2019.sort_values('CiteScore', ascending = False)
Top_10_CS = sort_2019_CS['Source title'][0:10]

# Sort by SJR and find the top 10 for 2019
sort_2019_SJR = kaggle2019.sort_values('SJR', ascending = False)
Top_10_SJR = sort_2019_SJR['Source title'][0:10]

# Sort by SNIP and find the top 10 for 2019
sort_2019_SNIP = kaggle2019.sort_values('SNIP', ascending = False)
Top_10_SNIP = sort_2019_SNIP['Source title'][0:10]

# Find the entries for the top 10 in 5 previous years. Not all entries may match 
# Top 10 CiteScore in 2019
Top_CS_merge = kaggle_merge[kaggle_merge['Source title'].isin(Top_10_CS)]
Top_CS_merge=Top_CS_merge.rename(columns = {'CiteScore_2015':'2015','CiteScore_2016':'2016',
                                            'CiteScore_2017':'2017','CiteScore_2018':'2018','CiteScore':'2019'})
# Rename long journals to something easier to read
Top_CS_merge['Source title'] = Top_CS_merge['Source title'].replace(['MMWR. Surveillance summaries : Morbidity and mortality weekly report. Surveillance summaries / CDC','Source title'],'MMWR. Surveillance summaries')
# Use Pandas' DataFrame .melt method to restructure the data into long form for use with Seaborn
Top_CS_merge_melt = pd.melt(Top_CS_merge, id_vars=('Source title'),
                            value_vars=['2015','2016','2017','2018','2019'],var_name='Year', value_name='CiteScore')

# Top 10 SJR in 2019
Top_SJR_merge = kaggle_merge[kaggle_merge['Source title'].isin(Top_10_SJR)]
Top_SJR_merge=Top_SJR_merge.rename(columns = {'SJR_2015':'2015','SJR_2016':'2016',
                                              'SJR_2017':'2017','SJR_2018':'2018','SJR':'2019'})
# Rename long journals to something easier to read
Top_SJR_merge['Source title'] = Top_SJR_merge['Source title'].replace(['National vital statistics reports : from the Centers for Disease Control and Prevention, National Center for Health Statistics, National Vital Statistics System'],'National vital statistics reports')
# Use Pandas' DataFrame .melt method to restructure the data into long form for use with Seaborn
Top_SJR_merge_melt = pd.melt(Top_SJR_merge, id_vars=('Source title'), 
                             value_vars=['2015','2016','2017','2018','2019'],var_name='Year', value_name='SJR')

# Top 10 SNIP in 2019
Top_SNIP_merge = kaggle_merge[kaggle_merge['Source title'].isin(Top_10_SNIP)]
Top_SNIP_merge=Top_SNIP_merge.rename(columns = {'SNIP_2015':'2015','SNIP_2016':'2016',
                                                'SNIP_2017':'2017','SNIP_2018':'2018','SNIP':'2019'})
# Rename long journals to something easier to read
Top_SNIP_merge['Source title'] = Top_SNIP_merge['Source title'].replace(['MMWR. Surveillance summaries : Morbidity and mortality weekly report. Surveillance summaries / CDC','Source title'],'MMWR. Surveillance summaries')
Top_SNIP_merge['Source title'] = Top_SNIP_merge['Source title'].replace(['National vital statistics reports : from the Centers for Disease Control and Prevention, National Center for Health Statistics, National Vital Statistics System'],'National vital statistics reports')
# Use Pandas' DataFrame .melt method to restructure the data into long form for use with Seaborn
Top_SNIP_merge_melt = pd.melt(Top_SNIP_merge, id_vars=('Source title'), 
                              value_vars=['2015','2016','2017','2018','2019'],var_name='Year', value_name='SNIP')


# Plots for Top journals in 2019 that have data for the previous 5 years
plt.figure()

Top_8_CS_plot = sns.catplot(data = Top_CS_merge_melt, x = 'Year', y= 'CiteScore', kind = 'point', hue = 'Source title')

Top_8_CS_plot.set_xticklabels(rotation = 45)
Top_8_CS_plot.set_ylabels('CiteScore')
Top_8_CS_plot.set_xlabels('Year')
Top_8_CS_plot.fig.suptitle("Point Plot of CiteScore vs Year for the Top 7 Journals from 2019", y = 1.05)
Top_8_CS_plot.fig.text(0.05, 1.05,"(a)",fontdict=dict(size=16))
Top_8_CS_plot.savefig('Images\\Top_8_CiteScore_2015-2019.png',dpi = 300)

Top_7_SNIP_plot = sns.catplot(data = Top_SNIP_merge_melt, x = 'Year', y= 'SNIP', kind = 'point', hue = 'Source title')

Top_7_SNIP_plot.set_xticklabels(rotation = 45)
Top_7_SNIP_plot.set_ylabels('SNIP')
Top_7_SNIP_plot.set_xlabels('Year')
Top_7_SNIP_plot.fig.suptitle("Point Plot of SNIP vs Year for the Top 7 Journals from 2019", y = 1.05)
Top_7_SNIP_plot.fig.text(0.05, 1.05,"(b)",fontdict=dict(size=16))
Top_7_SNIP_plot.savefig('Images\\Top_7_SNIP_2015-2019.png',dpi = 300)

Top_7_SJR_plot = sns.catplot(data = Top_SJR_merge_melt, x = 'Year', y= 'SJR', kind = 'point', hue = 'Source title')

Top_7_SJR_plot.set_xticklabels(rotation = 45)
Top_7_SJR_plot.set_ylabels('SJR')
Top_7_SJR_plot.set_xlabels('Year')
Top_7_SJR_plot.fig.suptitle("Point Plot of SJR vs Year for the Top 8 Journals from 2019", y = 1.05)
Top_7_SJR_plot.fig.text(0.05, 1.05,"(c)",fontdict=dict(size=16))
Top_7_SJR_plot.savefig('Images\\Top_8_SJR_2015-2019.png',dpi = 300)
