# -*- coding: utf-8 -*-
"""
Created on Tue Nov  9 16:30:18 2021

@author: markj
"""

import os
import time
from sqlalchemy import create_engine 
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
from PMed_to_DF import Create_ISSN

tic = time.perf_counter()
# Get current working directory and save as cwd
cwd = os.getcwd()

# Create the sqlalchemy engine using create_engine() method
engine = create_engine('sqlite:///' + cwd + '\\impactfactor.db')


# The first addition to the database is from a Kaggle file. 
# I use an API to download the file then clean the data and add to the database
# Initialise kaggle api and then download the file needed
api = KaggleApi()
api.authenticate()
api.dataset_download_file('umairnasir14/impact-factor-of-top-1000-journals','Impact-Factor-Ratings.xlsx')

IFR_path= "Impact-Factor-Ratings.xlsx"
# This loads in all sheets of 'Impact-Factor-Ratings.xlsx' as JIF
IFR = pd.read_excel(IFR_path,index_col=None,sheet_name=None)
# This loop renames the columns appropriately. The name of each sheet is a year we construct a new string to use from i in the loop.
for i in IFR:
    keyname = str(int(i)-3) + '-' + str(int(i)-2000)
    IFR[str(i)] = IFR[str(i)].rename(columns={keyname+' Citations':'Citations', keyname+' Documents':'Documents'})
# This part of the loop fixes the Highest Percentile column which has concatenated 3 types. I'm only interested in keeping the subject areas
    IFR[str(i)]['tempcol'] = IFR[str(i)]['Highest percentile'].str.split('\n')
    IFR[str(i)]['Subjects']=IFR[str(i)]['tempcol'].str[2]  
    IFR[str(i)].drop(['tempcol'], axis=1, inplace=True)   
# This part of the loop finds keys with na values and then create a new JIF for each key with the na rows removed
    keys_with_na = IFR[str(i)].keys()[IFR[str(i)].isna().any()]
    for j in keys_with_na:
        IFR[str(i)] = IFR[str(i)][IFR[str(i)][j].isna()==False]
# This part of the loop saves each file to the database
    IFR[str(i)].to_sql('kaggledata'+str(i), engine)
 
 
# The next addition to the database is a datafile from PubMed. The data from 
# pubmed is in a .txt format which needed extensive reformatting so I wrote a 
# function (PMed_to_DF.py) which I import to restructure the data. This was imported earlier from another file
# The function can take an integer to determine how many entries to take, but if left blank it defaults to the max (34371)
PMed = Create_ISSN()
PMed.to_sql('PubMed', engine)


#The next source of data for the database is from InCites. This stores the actual journal impact factor data.
InCites_path="JCR2021.xlsx"
#Data is imported from the Excel file and rows are renamed
InCites = pd.read_excel(InCites_path,skiprows=2,index_col=None, names = (['Journal_Title', 'Total_Citations', 'JIF', 'ES']))
# The data is cleaned to remove values = 0 or those where there is a specific string
# Any rows with na values are dropped
InCites=InCites.dropna()
# any rows with JIF = 0 or JIF = the string 'Not Available' are removed
InCites = InCites[((InCites['JIF']!=0) & (InCites['JIF']!='Not Available'))]
# Added to database
InCites.to_sql('Incites', engine)


# To supplement the Kaggle data, I downloaded the full Scopus database which 
# goes past the first 1000 entries and also contains data for 2020. 

# For the purpose of this project I only take the 2020 sheet. 
# The Scopus data seems to be complete so little cleaning is needed.

# Note that this data has multiple duplicate columns since each Scopus Sub-Subject Area
# is a separate entry for each journal.
scopus_path="Scopus.xlsb"
scopus = pd.read_excel(scopus_path,sheet_name = 1,names=(['Scopus Source ID', 'Journal_Title', 'Citation Count', 'Documents',
       'Percent Cited', 'CiteScore', 'SNIP', 'SJR',
       'Subjects', 'Scopus Sub-Subject Area',
       'Percentile', 'RANK', 'Rank Out Of', 'Publisher', 'Type', 'Open Access',
       'Quartile', 'Top 10% (CiteScore Percentile)', 'URL Scopus Source ID',
       'ISSN', 'eISSN']))

# Add to database
scopus.to_sql('Scopus', engine)


#SCIE Journals (I didn't end up using this, but the data is still valuable so I'll keep it in the database in case I plan on using it later)
SCIE_path = 'wos-core_SCIE 2021-October-21.csv'
SCIE = pd.read_csv(SCIE_path,skiprows=1,names = ['Journal_Title', 'ISSN', 'eISSN', 'Publisher', 'Publisher Address', 'Languages', 'Scientific_Categories'])
SCIE.to_sql('SCIE', engine)


toc = time.perf_counter()   
print(f"DataFrame populated in {toc - tic:0.4f} seconds")



