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
scopus= pd.read_sql_query('SELECT "Journal_Title", Publisher, "Citation_Count", Documents, CiteScore, SNIP, SJR FROM Scopus', engine)

# Load SCIE data

# Load PMed data

plt.figure()