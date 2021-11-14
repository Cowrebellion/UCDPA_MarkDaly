# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 22:20:04 2021

@author: markj
"""

import pandas as pd
import matplotlib.pyplot as plt

jcr = pd.read_excel('JCR2021.xlsx',skiprows=2,index_col=0, names = (['Journal_Title', 'Total_Citations', 'JIF', 'ES']))
SCIE_journals = pd.read_csv('wos-core_SCIE 2021-October-21.csv',skiprows=1,names = ['Journal_Title', 'ISSN', 'eISSN', 'Publisher', 'Publisher Address', 'Languages', 'Scientific_Categories'])


jcr['Journal_Title']=jcr['Journal_Title'].str.lower()
SCIE_journals['Journal_Title']=SCIE_journals['Journal_Title'].str.lower()

merged_jcr = jcr.merge(SCIE_journals, on = 'Journal_Title', how = 'left')
merged_jcr=merged_jcr.dropna()
merged_jcr = merged_jcr[((merged_jcr['JIF']!=0) & (merged_jcr['JIF']!='Not Available'))]

merged_jcr['JIF']=merged_jcr['JIF'].astype("float")
merged_jcr['Documents'] = merged_jcr['Total_Citations']/merged_jcr['JIF']


merged_jcr.plot('Documents','JIF', kind = 'scatter')
plt.xlabel('# Publications')
plt.ylabel('Impact Factor')
plt.ylim(0,110)
plt.xlim(0,20000)

#merged_jcr['Documents']=merged_jcr['Total_Citations']/merged_jcr['JIF']
# print (JCR.head())
# print(JCR.keys())
# print(type(JCR))

# print(SCIE_journals['Journal title'])
# print (SCIE_journals.head())
# print(SCIE_journals.keys())
# print(type(SCIE_journals))