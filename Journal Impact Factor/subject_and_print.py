# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 12:41:55 2021

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

# Set seaborn style and context

sns.set_style("darkgrid")
sns.set_context("paper")
# setting dpi resolution for later figure exports
resol = 300

def pcnt(df_col,pct):
    return np.percentile(df_col,pct)
    

# Create the db engine using create_engine() method
engine = create_engine('sqlite:///' + cwd + '\\impactfactor.db')

# Load Scopus 2020 data taking only the relevant columns from impactfactor.db    
scopus= pd.read_sql_query('SELECT "Journal_Title", Publisher, Documents, SNIP FROM Scopus', engine)
# Remove duplicates since we aren't including all columns
scopus = scopus.drop_duplicates()

# Load PubMed data taking only the relevant columns from impactfactor.db    
pubmed= pd.read_sql_query('SELECT "Journal_Title",ISSN, eISSN FROM PubMed', engine)

#set "Journal_Title" to lowercase to increase chance of merging on this index
scopus['Journal_Title']=scopus['Journal_Title'].str.lower()
pubmed['Journal_Title']=pubmed['Journal_Title'].str.lower()


# inner join on data to only keep matching pairs
merged_data_pubtype = scopus.merge(pubmed, on = "Journal_Title" )
# I want a new column that indicats if a journal publishes in print only, online only, or both

merged_data_pubtype.loc[((merged_data_pubtype['ISSN']!="")&(merged_data_pubtype['eISSN']=="")),"Type"]='Print'
merged_data_pubtype.loc[((merged_data_pubtype['eISSN']!="")&(merged_data_pubtype['ISSN']=="")),"Type"]='Online'
merged_data_pubtype.loc[((merged_data_pubtype['eISSN']!="")&(merged_data_pubtype['ISSN']!="")),"Type"]='Mixed'

# Plot scatter plots for each publishing type
pub_type = sns.FacetGrid(data = merged_data_pubtype, col="Type")
pub_type.map(sns.scatterplot, 'Documents', 'SNIP')
pub_type.fig.suptitle("Scatterplots of Documents Published vs SNIP for Journal Types (2020 data)", y = 1.05)
# Save Figure
pub_type.savefig('Images\\2020 PubType',dpi = 300)
# Clear figure and create a new one
plt.clf()
plt.figure()

# Load Scopus Data again, but with subject information


scopus= pd.read_sql_query('SELECT "Journal_Title", Publisher, Documents, SNIP, "Scopus Sub-Subject Area" FROM Scopus', engine)

# The Scopus data contains information about the subjects, but they are in strings. I need to change this to a list first
scopus["Scopus Sub-Subject Area"] = scopus["Scopus Sub-Subject Area"].str.split(',|and ')
# A column of lists is not a good way to store data so I will use .explode to put this in long form
scopus_explode = scopus.explode("Scopus Sub-Subject Area")
# Remove a few blank entries
scopus_explode = scopus_explode[scopus_explode["Scopus Sub-Subject Area"]!=' ']
# Group by subject, then sort by number of Documents published in 2020
scopus_explode_grouped = scopus_explode.groupby("Scopus Sub-Subject Area").sum()
scopus_explode_grouped = scopus_explode_grouped.sort_values('Documents',ascending = False)
# Top 10 Subjects by publication volume
Top10 = scopus_explode_grouped[0:10]
Top10=Top10.reset_index()

# Create a Bar Chart of the Top 10 Subjects in 2020 by publication volume
top10_bar = sns.barplot(data = Top10, x = "Scopus Sub-Subject Area",  y = 'Documents')
plt.xticks(rotation=45,horizontalalignment='right')
plt.title("Top 10 Subjects by Publication Volume")

plt.savefig('Images\\Top 10',dpi = 300,bbox_inches = "tight")