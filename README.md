# UCDPA_MarkDaly

This is my submission to the UCDPA course on Introductory Data Analytics.

My submission uses a number of data sources from Scopus, InCites, PubMed and Kaggle to provide some insights into Journal-based metrics using pandas, sqlalchemy, matplotlib, numpy and seaborn. 

DB_Create.py creates a database called impactfactor.db from the various data files in the same directory as this python file
Kaggle_metrics.py Creates graphs using the data from a file taken from Kaggle (https://www.kaggle.com/umairnasir14/impact-factor-of-top-1000-journals)
Scopus_data_JIF.py  plots some graphs using data from SCOPUS and InCites 
subject_and_print.py plots graphs using Scopus data combined with PubMed data. 

Please note that some of the operations performed in this project may seem redundant, but to complete the project brief a number of techniques needed to be used. I am aware that the Scopus data also contains ISSN information. 

The Kaggle data is a subset of the data available freely on Scopus, but the Scopus data was discovered later.

Please let me know if you find any of these plots of interest to you! I plan to expand more this in the future using some additoinal techniques and better data.
