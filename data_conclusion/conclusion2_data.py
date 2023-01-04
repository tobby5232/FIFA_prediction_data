# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 16:03:22 2023

@author: ch406
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import ConnectionPatch
from datetime import datetime, timedelta


#%%
# Import result data
df_result = pd.read_csv('winter_wining_rate.csv')

#Simplifized date formate to year only
df_result.insert(0,'Year',None)
for i in range(len(df_result["date"])):
    df_result["Year"][i]=df_result["date"][i][:4]
df_result["Year"]=df_result["Year"].astype(int)

#Simplifized dataFrame only world cup betewwn 2006~2018
df_result=df_result[df_result['Year'] >=2006]
df_result['date'] = pd.to_datetime(df_result['date'])


# print(df_result.head())

#%%
#Import team ranking & Country_code
df_ranking = pd.read_csv('AllTime_ranking.csv')
df_country_code = pd.read_csv('Country_code.csv')

#Replace contary_code as full country name in df_ranking
df_ranking_merge = df_ranking.merge(df_country_code, how='inner', indicator=False)

#Filter top10 teams in df_ranking_merge
df_ranking_merge=df_ranking_merge[['Country','Year','Previous_Rank','Total_Points','Country_Code']]
df_ranking_top=df_ranking_merge[df_ranking_merge['Previous_Rank'] <=10]
df_ranking_top=df_ranking_top.reset_index()

print(df_ranking_top.info())

#%%
#Import team ranking

df_result.insert(len(df_result.columns),'home_ranking',None)
df_result.insert(len(df_result.columns),'away_ranking',None)
df_result=df_result.drop("tournament",axis=1)
df_result=df_result.drop("city",axis=1)
df_result=df_result.drop("country",axis=1)
df_result=df_result.drop("neutral",axis=1)
df_result=df_result.reset_index(drop=True)

# print(df_result.info())

#%%
#Filter top10 teams in df_result

for i in range(len(df_result)):
    for j in range(len(df_ranking_top)):
        if df_result['home_team'][i]==df_ranking_top['Country'][j]:
            df_result['home_ranking'][i]=df_ranking_top['Previous_Rank'][j]
        if df_result['away_team'][i]==df_ranking_top['Country'][j]:
            df_result['away_ranking'][i]=df_ranking_top['Previous_Rank'][j]
print(df_result.info())

#%%
#Drop match without top 10 teams

df_result_top10=df_result.copy()
for i in range(len(df_result_top10)):
    if df_result['home_ranking'][i]==None and df_result['away_ranking'][i]==None :
        # print(type(df_result['home_ranking'][i]))
        # print(type(df_result['away_ranking'][i]))
        df_result_top10=df_result_top10.drop(i)
df_result_top10=df_result_top10.reset_index(drop=True)


print(df_result_top10.info())

#%%
#Insert rank/goal_dif
df_result_top10.insert(len(df_result_top10.columns),'rank_dif',None)
df_result_top10.insert(len(df_result_top10.columns),'goal_dif',None)

for i in range(len(df_result_top10)):
    if (df_result_top10['home_ranking'][i]!=None and df_result_top10['away_ranking'][i]!=None):
        df_result_top10['rank_dif'][i] = df_result_top10['home_ranking'][i]-df_result_top10['away_ranking'][i]
        # print(df_result_top10['rank_dif'][i])
df_result_top10['goal_dif'] = df_result_top10.apply(lambda x: x['home_score'] - x['away_score'], axis = 1)
print(df_result_top10.info())

#%%
# for i in range(len(df_result_top10)):
#     print(df_result['away_ranking'][i])

#%%
#Output df_result_top10

df_result_top10.to_csv("result_top10.csv", index = True)