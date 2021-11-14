# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 13:53:44 2021

@author: markj
"""

from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#import openpyxl
from PMed_to_DF import Create_ISSN

api = KaggleApi()
api.authenticate()
api.dataset_download_file('umairnasir14/impact-factor-of-top-1000-journals','Impact-Factor-Ratings.xlsx')

def prcntl(col, pct):
    return col.quantile(pct)

# def pct75(column):
#     return column.quantile(0.75)

# def pct90(column):
#     return column.quantile(0.90)


IFR_path= "Impact-Factor-Ratings.xlsx"

JIF = pd.read_excel(IFR_path,index_col=None)
JIF = JIF.rename(columns={'2016-19 Citations':'Citations', "2016-19 Documents":'Documents'})
# #print(JIF.head())
# #print(JIF.keys())
# print("JIF mean from top 1000 is: ", JIF['SJR'].mean())

# plt.hist(JIF['SJR'],bins=100,range= [0,100])
#print(JIF['CiteScore'].max())
print("The 50th percentile is: ",prcntl(JIF['CiteScore'],.5),"\n")

# #print(JIF[JIF['SJR'].isnull()])

JIF_publisher = JIF.groupby('Publisher').mean()
# print("Springer Nature's aggregrate data (within first 1000) is: \n",JIF_publisher.loc['Springer Nature'])
# print(JIF_publisher.sort_values(by=['SJR']))
#JIF_publisher.plot('Documents','CiteScore', kind = 'scatter')
#plt.xlabel('# Publications')
#plt.ylabel('Impact Factor')
#plt.ylim(0,110)
#plt.xlim(0,20000)
#plt.hlines(prcntl(JIF['CiteScore'],.5),0,20000, colors = 'red', linestyles = 'dashed')
#plt.hlines(prcntl(JIF['CiteScore'],.9),0,20000, colors = 'black', linestyles = 'dashed')
#plt.hlines(prcntl(JIF['CiteScore'],.99),0,20000, colors = 'green', linestyles = 'dashed')
#plt.vlines(prcntl(JIF['Documents'],.5),0,120, colors = 'blue', linestyles = 'dashed')


#print(JIF[JIF['CiteScore']<pct50(JIF['CiteScore'])][['Source title','CiteScore']].count())
#print(JIF[JIF['CiteScore']>pct50(JIF['CiteScore'])][['Source title','CiteScore']].count())


#plt.bar(JIF_publisher.keys(),JIF_publisher.loc['Springer Nature'])

#ISSN = Create_ISSN(100)
#print(ISSN)

jcr = pd.read_excel('JCR2021.xlsx',skiprows=2,index_col=0, names = (['Journal_Title', 'Total_Citations', 'JIF', 'ES']))
SCIE_journals = pd.read_csv('wos-core_SCIE 2021-October-21.csv',skiprows=1,names = ['Journal_Title', 'ISSN', 'eISSN', 'Publisher', 'Publisher Address', 'Languages', 'Scientific_Categories'])


jcr['Journal_Title']=jcr['Journal_Title'].str.lower()
SCIE_journals['Journal_Title']=SCIE_journals['Journal_Title'].str.lower()

merged_jcr = jcr.merge(SCIE_journals, on = 'Journal_Title', how = 'left')
merged_jcr = merged_jcr.dropna()
merged_jcr = merged_jcr[~(merged_jcr['JIF']=="Not Available") | (merged_jcr['JIF']==0)]

merged_jcr['JIF']=merged_jcr['JIF'].astype("float")
merged_jcr['Documents'] = merged_jcr['Total_Citations']/merged_jcr['JIF']


merged_jcr.plot('Documents','JIF', kind = 'scatter')
plt.xlabel('# Publications')
plt.ylabel('Impact Factor')
plt.ylim(0,110)
plt.xlim(0,20000)
plt.hlines(prcntl(merged_jcr['JIF'],.9),0,20000, colors = 'black', linestyles = 'dashed')
plt.hlines(prcntl(merged_jcr['JIF'],.99),0,20000, colors = 'green', linestyles = 'dashed')
plt.vlines(prcntl(merged_jcr['Documents'],.5),0,120, colors = 'blue', linestyles = 'dashed')
plt.show()