# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 16:15:36 2022

@author: ch406
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import ConnectionPatch


#%%
# Import xG data
df_score_time = pd.read_csv('score_timing.csv')

# print(df_score_time.info())

#%%
#Countion every goal timing
score_timing=[]

for i in range(len(df_score_time)):
    if type(df_score_time['home_team_goal_timings'][i]) is str:
        df_score_time['home_team_goal_timings'][i]=df_score_time['home_team_goal_timings'][i].split(',')
        for j in range(len(df_score_time['home_team_goal_timings'][i])):
            score_timing.append(df_score_time['home_team_goal_timings'][i][j])
    if type(df_score_time['away_team_goal_timings'][i]) is str:
        df_score_time['away_team_goal_timings'][i]=df_score_time['away_team_goal_timings'][i].split(',')
        for j in range(len(df_score_time['away_team_goal_timings'][i])):
            score_timing.append(df_score_time['away_team_goal_timings'][i][j])
        
print(len(score_timing))

#%%
#Countion extra goal timing
extra_time=0

for i in range(len(score_timing)):
    extra_time+=score_timing[i].count("'")
print(extra_time)
# print(df_score_time.info())

#%%
#Import team ranking & Country_code
df_ranking = pd.read_csv('AllTime_ranking.csv')
df_country_code = pd.read_csv('Country_code.csv')

#Replace contary_code as full country name in df_ranking
df_ranking_merge = df_ranking.merge(df_country_code, how='inner', indicator=False)
df_ranking_merge=df_ranking_merge[df_ranking_merge['Year']==2022]
df_ranking_merge=df_ranking_merge[['Year','Country','Previous_Rank','Country_Code']]
df_ranking_merge=df_ranking_merge.reset_index()
# print(df_ranking_merge.head())

#%%
#Import ranking data to df_score_time
rank_home=[]
rank_away=[]
Country_Code_home=[]
Country_Code_away=[]
Insert_title=['rank_home','rank_away','Country_Code_home','Country_Code_away']
Insert_column=[rank_home,rank_away,Country_Code_home,Country_Code_away]

for i in range(len(df_score_time)):
    # df_score_time['stadium_name'][i]='N'
    df_score_time["home_team_name"][i]=df_score_time["home_team_name"][i].replace("USMNT", "United States")
    df_score_time["away_team_name"][i]=df_score_time["away_team_name"][i].replace("USMNT", "United States")
    for j in range(len(df_ranking_merge)):
        if df_score_time['home_team_name'][i]==df_ranking_merge['Country'][j]:
            rank_home.append(df_ranking_merge['Previous_Rank'][j])
            Country_Code_home.append(df_ranking_merge['Country_Code'][j])
            # df_score_time['stadium_name'][i]='Y'
        if df_score_time['away_team_name'][i]==df_ranking_merge['Country'][j]:
            rank_away.append(df_ranking_merge['Previous_Rank'][j])
            Country_Code_away.append(df_ranking_merge['Country_Code'][j])
            # df_score_time['stadium_name'][i]='Y'
            
for k in range(len(Insert_title)):
    df_score_time.insert(len(df_score_time.columns),Insert_title[k],Insert_column[k])
# print(df_score_time.info())

#%%
#Ranking different

df_score_time['ranking_dif'] = df_score_time.apply(lambda x: x['rank_home'] - x['rank_away'], axis = 1)
df_score_time['goal_dif'] = df_score_time.apply(lambda x: x['home_team_goal_count'] - x['away_team_goal_count'], axis = 1)
print(df_score_time.info())

#%%
#Calculate stronger team winning rate
df_stronger_team=df_score_time.copy()
df_stronger_team=df_stronger_team[['home_team_name','away_team_name','ranking_dif','goal_dif']]
df_stronger_team.insert(len(df_stronger_team.columns),'result_strong_team',None)

for i in range (len(df_stronger_team)):
    if df_stronger_team['ranking_dif'][i]<0:
        if df_stronger_team['goal_dif'][i]>0:
            df_stronger_team['result_strong_team'][i]='win'
        elif df_stronger_team['goal_dif'][i]<0:
            df_stronger_team['result_strong_team'][i]='lose'
        else:
            df_stronger_team['result_strong_team'][i]='draw'
    elif df_stronger_team['ranking_dif'][i]>0:
        if df_stronger_team['goal_dif'][i]>0:
            df_stronger_team['result_strong_team'][i]='lose'
        elif df_stronger_team['goal_dif'][i]<0:
            df_stronger_team['result_strong_team'][i]='win'
        else:
            df_stronger_team['result_strong_team'][i]='draw'
            
from collections import Counter

countiong=Counter(df_stronger_team['result_strong_team'])

win=countiong['win']
draw=countiong['draw']
lose=countiong['lose']

# print(countiong)
print(win,lose,draw)

#%%
#Draw pie chart for strong team winning rate in 2022 WC

fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"),dpi=500)


data = [win/64,draw/64,lose/64]
data=[round(i,3)*100 for i in data]
ingredients = ['winning_rate','draw_rate','lose_rate']


def func(pct, allvals):
    absolute = int(np.round(pct/10000.*np.sum(allvals)*64))
    return "{:.1f}%\n({:d} games)".format(pct, absolute)

color1=['#01B468','#A6FFA6','#EA0000']
wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                  colors=color1,
                                  textprops=dict(color="black",size='1'))

ax.legend(wedges, ingredients,
          loc="best",
          fontsize=5)

plt.setp(autotexts, size=8, weight="bold")

ax.set_title("Top team winning rate\nin 2022 world cup",
             fontsize=7)

plt.show()

#%%
#Score timing for weak team
score_timing_weak=[]
weak_team_wining=0

for i in range(len(df_score_time)):
    if df_score_time['ranking_dif'][i]>0:
        if df_score_time['goal_dif'][i]>0:
            weak_team_wining+=1
        if type(df_score_time['home_team_goal_timings'][i]) is list:
            for j in range(len(df_score_time['home_team_goal_timings'][i])):
                score_timing_weak.append(df_score_time['home_team_goal_timings'][i][j])
    elif df_score_time['ranking_dif'][i]<0:
        if df_score_time['goal_dif'][i]<0:
            weak_team_wining+=1
        if type(df_score_time['away_team_goal_timings'][i]) is list:
            for j in range(len(df_score_time['away_team_goal_timings'][i])):
                score_timing_weak.append(df_score_time['away_team_goal_timings'][i][j])
            
# print(len(score_timing_weak))
# print(weak_team_wining)
            
#%%
#Countion weak_team extra goal timing
weak_extra_time=0

for i in range(len(score_timing_weak)):
    weak_extra_time+=score_timing_weak[i].count("'")
# print(weak_extra_time)

#%%
#Conclusion
print('world cup total goal :',len(score_timing))
print('world cup total goal at extra time:',extra_time)
print('world cup total goal for weak team:',len(score_timing_weak))
print('world cup total goal for weak team at extra time:',weak_extra_time)
print('weak team winning time:',weak_team_wining)


#%%

# make figure and assign axis objects
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 5),dpi=500)
fig.subplots_adjust(wspace=0)

# pie chart parameters
overall_ratios = [extra_time/len(score_timing),(len(score_timing)-extra_time)/len(score_timing)]
labels = ['Goal at extra_time', 'Goal at regular_time']
inner_ratios = [len(score_timing_weak)/len(score_timing),(len(score_timing)-len(score_timing_weak))/len(score_timing)]
labels2 = ['Goal for weak team', 'Goal for stronger team']
explode = [0.1, 0]
size = 0.4

#pir chart color
cmap = plt.colormaps["tab20c"]
outer_colors = cmap(np.arange(3)*4)
inner_colors = cmap([1, 2, 5, 6, 9, 10])

# rotate so that first wedge is split by the x-axis
angle = -180 * overall_ratios[0]
wedges, *_ = ax1.pie(overall_ratios,radius=1.05,autopct='%1.1f%%', pctdistance=0.8, startangle=angle,labeldistance =None,
                     labels=labels, explode=explode,wedgeprops=dict(width=size*2, edgecolor='w'))
wedges2, *_=ax1.pie(inner_ratios, autopct='%1.1f%%', startangle=angle,colors=inner_colors, labeldistance=None,
                    labels=labels2,radius=1-size,wedgeprops=dict(width=size, edgecolor='w'),
                      textprops=dict(color="b"))
ax1.legend( loc="upper left",fontsize=7)
ax1.set_title('Goal time ratio')

# bar chart parameters
age_ratios = [weak_extra_time/extra_time,(extra_time-weak_extra_time)/extra_time]
age_labels = ['Weak team', 'Stronger team']
bottom = 1
width = .2

# Adding from the top matches the legend.
for j, (height, label) in enumerate(reversed([*zip(age_ratios, age_labels)])):
    bottom -= height
    bc = ax2.bar(0, height, width, bottom=bottom, color='C0', label=label,
                 alpha=0.1 + 0.25 * j)
    ax2.bar_label(bc, labels=[f"{height:.0%}"], label_type='center')

ax2.set_title('Extra_time goal ratio')
ax2.legend(fontsize=7)
ax2.axis('off')
ax2.set_xlim(- 2 * width, 2.5 * width)


# use ConnectionPatch to draw lines between the two plots
theta1, theta2 = wedges[0].theta1, wedges[0].theta2
center, r = wedges[0].center, wedges[0].r
bar_height = sum(age_ratios)

# draw top connecting line
x = r * np.cos(np.pi / 180 * theta2) + center[0]
y = r * np.sin(np.pi / 180 * theta2) + center[1]
con = ConnectionPatch(xyA=(-width / 2, bar_height), coordsA=ax2.transData,
                      xyB=(x, y), coordsB=ax1.transData)
con.set_color([0, 0, 0])
con.set_linewidth(4)
ax2.add_artist(con)

# draw bottom connecting line
x = r * np.cos(np.pi / 180 * theta1) + center[0]
y = r * np.sin(np.pi / 180 * theta1) + center[1]
con = ConnectionPatch(xyA=(-width / 2, 0), coordsA=ax2.transData,
                      xyB=(x, y), coordsB=ax1.transData)
con.set_color([0, 0, 0])
ax2.add_artist(con)
con.set_linewidth(4)

plt.show()