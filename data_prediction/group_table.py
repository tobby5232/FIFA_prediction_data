# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 20:52:04 2022

@author: ch406
"""

import pandas as pd

#%%
#All group list
all_group_list=[['Group_A','Netherlands',0,0,0,0],['Group_A','Senegal',0,0,0,0],['Group_A','Ecuador',0,0,0,0],['Group_A','Qatar',0,0,0,0],
               ['Group_B','England',0,0,0,0],['Group_B','United States',0,0,0,0],['Group_B','Iran',0,0,0,0],['Group_B','Wales',0,0,0,0],
               ['Group_C','Argentina',0,0,0,0],['Group_C','Mexico',0,0,0,0],['Group_C','Poland',0,0,0,0],['Group_C','Saudi Arabia',0,0,0,0],
               ['Group_D','France',0,0,0,0],['Group_D','Denmark',0,0,0,0],['Group_D','Tunisia',0,0,0,0],['Group_D','Australia',0,0,0,0],
               ['Group_E','Germany',0,0,0,0],['Group_E','Spain',0,0,0,0],['Group_E','Japan',0,0,0,0],['Group_E','Costa Rica',0,0,0,0],
               ['Group_F','Belgium',0,0,0,0],['Group_F','Croatia',0,0,0,0],['Group_F','Morocco',0,0,0,0],['Group_F','Canada',0,0,0,0],
               ['Group_G','Brazil',0,0,0,0],['Group_G','Serbia',0,0,0,0],['Group_G','Switzerland',0,0,0,0],['Group_G','Cameroon',0,0,0,0],
               ['Group_H','Portugal',0,0,0,0],['Group_H','Uruguay',0,0,0,0],['Group_H','Ghana',0,0,0,0],['Group_H','South Korea',0,0,0,0]]

#%%
all_group_df = pd.DataFrame(all_group_list,columns=['group','Nation','game','W','D','L'])
# all_group_df=all_group_df.T
all_group_df.set_index(keys = ["group","Nation"],inplace=True)
all_group_df.insert(len(all_group_df.columns), 'points', 0)
print(all_group_df)

all_group_df.to_csv("group_table.csv")