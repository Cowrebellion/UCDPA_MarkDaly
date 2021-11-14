# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 21:02:47 2021

@author: markj
"""

import pandas as pd


#PubMedFile="https://ftp.ncbi.nih.gov/pubmed/J_Medline.txt"
#Create blank dataframe with appropriate headings
def Create_ISSN(No_Journals=34371):

    ISSN = pd.DataFrame(columns=['Journal_Title', 'ISSN', 'eISSN'])
    #Open the J_Medline.text file and read in all the lines.
    #Once all lines read, the appropriate sections of the lines are appended to the ISSN DataFrame
    with open("J_Medline.txt") as f:
        lines = f.readlines()
        for i in range(0,No_Journals):
            temp={'Journal_Title':lines[i*8+2][len('JournalTitle: '):-1],
                  'ISSN':lines[i*8+4][len('ISSN (Print): '):-1],
                  'eISSN':lines[i*8+5][len('ISSN (Online): '):-1]}
            ISSN=ISSN.append(temp,ignore_index=True)
    return ISSN
    

    
    