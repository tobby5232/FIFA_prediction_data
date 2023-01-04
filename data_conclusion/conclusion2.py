# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 19:23:47 2023

@author: ch406
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import ConnectionPatch


#%%
# Import top10 data
df_result_top10 = pd.read_csv('result_top10.csv')

# print(df_result_top10.info())

#%%
#Extract date as mounth

for i in range(len(df_result_top10["date"])):
    df_result_top10["date"][i]=df_result_top10["date"][i][5:7]
df_result_top10["date"]=df_result_top10["date"].astype(int)

# print(df_result_top10.info())

#%%
#Catogory result type (win/draw/lose)


df_result_top10.insert(len(df_result_top10.columns),'Total_game',None)
df_result_top10.insert(len(df_result_top10.columns),'Stroger_team_win',None)
df_result_top10.insert(len(df_result_top10.columns),'Stroger_team_draw',None)
df_result_top10.insert(len(df_result_top10.columns),'Stroger_team_lose',None)

for i in range(len(df_result_top10)):
    # print(df_result_top10['away_ranking'][3])
    if df_result_top10['home_ranking'].notnull()[i] and df_result_top10['away_ranking'].notnull()[i]:
        if df_result_top10['rank_dif'][i]<0:
            if df_result_top10['goal_dif'][i]>0:
                df_result_top10['Total_game'][i]='1'
                df_result_top10['Stroger_team_win'][i]='win'
            elif df_result_top10['goal_dif'][i]==0:
                df_result_top10['Total_game'][i]='1'
                df_result_top10['Stroger_team_draw'][i]='draw'
            else:
                df_result_top10['Total_game'][i]='1'
                df_result_top10['Stroger_team_lose'][i]='lose'
        elif df_result_top10['rank_dif'][i]>=0:
            if df_result_top10['goal_dif'][i]>0:
                df_result_top10['Total_game'][i]='1'
                df_result_top10['Stroger_team_lose'][i]='lose'
            elif df_result_top10['goal_dif'][i]==0:
                df_result_top10['Total_game'][i]='1'
                df_result_top10['Stroger_team_draw'][i]='draw'
            else:
                df_result_top10['Total_game'][i]='1'
                df_result_top10['Stroger_team_win'][i]='win'
    elif df_result_top10['home_ranking'].notnull()[i]:
        if df_result_top10['goal_dif'][i]>0:
            df_result_top10['Total_game'][i]='1'
            df_result_top10['Stroger_team_win'][i]='win'
        elif df_result_top10['goal_dif'][i]==0:
            df_result_top10['Total_game'][i]='1'
            df_result_top10['Stroger_team_draw'][i]='draw'
        else:
            df_result_top10['Total_game'][i]='1'
            df_result_top10['Stroger_team_lose'][i]='lose'
    else:
        if df_result_top10['goal_dif'][i]>0:
            df_result_top10['Total_game'][i]='1'
            df_result_top10['Stroger_team_lose'][i]='lose'
        elif df_result_top10['goal_dif'][i]==0:
            df_result_top10['Total_game'][i]='1'
            df_result_top10['Stroger_team_draw'][i]='draw'
        else:
            df_result_top10['Total_game'][i]='1'
            df_result_top10['Stroger_team_win'][i]='win'
            
print(df_result_top10.info())

# df_result_top10.to_csv("result_top10______.csv", index = None)
        
#%%
#Group df_result_top10 by mounth

df_group_result_top10=df_result_top10.groupby("date").count()

print(df_group_result_top10[['Total_game','Stroger_team_win','Stroger_team_draw','Stroger_team_lose']])

#%%
#List all time & summer & winter winner count.
def result_count(df_group_result_top10):
    Total_game=df_group_result_top10['Total_game'].sum()
    Total_win=df_group_result_top10['Stroger_team_win'].sum()
    Total_draw=df_group_result_top10['Stroger_team_draw'].sum()
    Total_lose=df_group_result_top10['Stroger_team_lose'].sum()
    return [Total_game,Total_win,Total_draw,Total_lose]

all_time_result=result_count(df_group_result_top10)
summer_result=result_count(df_group_result_top10[(df_group_result_top10.index == 6) | (df_group_result_top10.index == 7)])
winter_result=result_count(df_group_result_top10[(df_group_result_top10.index == 11) | (df_group_result_top10.index == 12)])

print('All_time_wining_rate:',all_time_result[1]/all_time_result[0])
print('Summer_time_wining_rate:',summer_result[1]/summer_result[0])
print('Winter_time_wining_rate:',winter_result[1]/winter_result[0])

#%%
#Def function for different month dataFrame

def sepResult (mon):
    result=result_count(df_group_result_top10[df_group_result_top10.index == mon])
    rsult_list=[result[3]/result[0], result[2]/result[0], result[1]/result[0]]
    rsult_list=[round(i,3)*100 for i in rsult_list]
    return rsult_list

Jan=sepResult(1)
Feb=sepResult(2)
Mar=sepResult(3)
Apr=sepResult(4)
May=sepResult(5)
Jun=sepResult(6)
Jul=sepResult(7)
Aug=sepResult(8)
Sep=sepResult(9)
Oct=sepResult(10)
Nov=sepResult(11)
Dec=sepResult(12)


#%%
#Plot bar chart for winning rate
All_time=[all_time_result[3]/all_time_result[0], all_time_result[2]/all_time_result[0], all_time_result[1]/all_time_result[0]]
All_time=[round(i,3)*100 for i in All_time]

category_names = ['lose_rate', 'draw_rate','winning_rate']
results = {
    'All_time':All_time,
    'Jan': Jan,
    'Feb':Feb,
    'Mar':Mar,
    'Apr':Apr,
    'May':May,
    'Jun':Jun,
    'Jul':Jul,
    'Aug':Aug,
    'Sep':Sep,
    'Oct':Oct,
    'Nov':Nov,
    'Dec':Dec
}


def survey(results, category_names):
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.colormaps['RdYlGn'](
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(9.2, 6),dpi=500)
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, height=0.5,
                        label=colname, color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        ax.bar_label(rects,fmt='%.1f%%', label_type='center', color=text_color)
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')

    return fig, ax


survey(results, category_names)
plt.show()

