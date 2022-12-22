# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 22:40:09 2022

@author: ch406
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re
import numpy as np

sns.set_style('darkgrid')


#%%
# Import all world cup odd
df_odd = pd.read_csv('WorldCupAndEuro_odd.csv')

#Modifed team name
for i in range(len(df_odd["Team1"])):
    df_odd["Team1"][i]=df_odd["Team1"][i].replace('\xa0', '')
    df_odd["Team2"][i]=df_odd["Team2"][i].replace('\xa0', '')
    df_odd["Team1"][i]=df_odd["Team1"][i].replace('&', 'and')
    df_odd["Team2"][i]=df_odd["Team2"][i].replace('&', 'and')
    df_odd["Team1"][i]=df_odd["Team1"][i].replace('USA', 'United States')
    df_odd["Team2"][i]=df_odd["Team2"][i].replace('USA', 'United States')
    df_odd["Team1"][i]=df_odd["Team1"][i].replace('Serbia and Montenegro', 'Serbia')
    df_odd["Team2"][i]=df_odd["Team2"][i].replace('Serbia and Montenegro', 'Serbia')
    df_odd["Team1"][i]=df_odd["Team1"][i].strip(' ')
    df_odd["Team2"][i]=df_odd["Team2"][i].strip(' ')

df_odd=df_odd.sort_values(by=['Team1','Team2'])
df_odd.rename(columns={'Year':'date','Team1':'home_team','Team2':'away_team'
                       ,'Team1_odd':'home_team_odd','Team2_odd':'away_team_odd'},inplace = True)
df_odd=df_odd.reset_index(drop=True)

# print(df_odd.info())

#%%
#Import all comptition result
df_result = pd.read_csv('results.csv')

#Simplifized date formate to year only
for i in range(len(df_result["date"])):
    df_result["date"][i]=df_result["date"][i][:4]
df_result["date"]=df_result["date"].astype(int)
year=df_result['date'].unique()

#Simplifized dataFrame only world cup betewwn 2006~2018
df_result=df_result[(df_result['date'] <2022) & (df_result['date'] >=2006) & ((df_result['tournament']=='FIFA World Cup') | (df_result['tournament']=='UEFA Euro'))]
df_result=df_result[['date','home_team','away_team','home_score','away_score']]

df_result=df_result.sort_values(by=['home_team','away_team'])
df_result=df_result.reset_index(drop=True)

# print(df_result.info())

#%%
# Check df_odd missing data

result1 = df_odd.merge(df_result, how='outer', indicator=True).loc[lambda x : x['_merge'] == 'left_only']
result1=result1[['date','home_team','away_team']].sort_values(by=['date','home_team','away_team'])

result2 = df_odd.merge(df_result, how='outer', indicator=True).loc[lambda x : x['_merge'] == 'right_only']
result2=result2[['date','home_team','away_team']].sort_values(by=['date','home_team','away_team'])
# print(result1)
# print('-'*150)
# print(result2)

#Merge two tables
df_OddAndResult = df_odd.merge(df_result, how='inner', indicator=False)
# print(df_OddAndResult.info())

#%%
#Add column result(win,lose,draw)

result_list=[]

for i in range(len(df_OddAndResult)):
    if df_OddAndResult['home_score'][i]>df_OddAndResult['away_score'][i]:
        result_list.append('win')
    elif df_OddAndResult['home_score'][i]<df_OddAndResult['away_score'][i]:
        result_list.append('lose')
    else:
        result_list.append('draw')

df_OddAndResult.insert(3,'result',result_list)

# print(df_OddAndResult.head())

#%%
#Add column goal difference

goal_difference=[]

for i in range(len(df_OddAndResult)):
    goal_diff=df_OddAndResult['home_score'][i]-df_OddAndResult['away_score'][i]
    goal_difference.append(goal_diff)

df_OddAndResult.insert(9,'goal_dif',goal_difference)

    
#%%
#Add column odd difference

odd_difference=[]

for i in range(len(df_OddAndResult)):
    odd_dif=df_OddAndResult['home_team_odd'][i]-df_OddAndResult['away_team_odd'][i]
    odd_difference.append(odd_dif)

df_OddAndResult.insert(10,'odd_dif',odd_difference)

print(df_OddAndResult.info())
# print(df_OddAndResult[['home_team_odd','away_team_odd','Draw_odd','odd_dif']].head(10))

#%%
#List all nation name(df_OddAndResult)
nation_name_home=df_OddAndResult['home_team'].unique()
nation_name_away=df_OddAndResult['away_team'].unique()

nation_name_list=np.concatenate([nation_name_home,nation_name_away])#Concat nparray
nation_name_set=set(nation_name_list)#Unique nparray
nation_name=list(nation_name_set)
nation_name.sort()

# print(nation_name)
# print(len(nation_name))

#%%
#Import team rating

df_rating = pd.read_csv('AllTeamRating.csv')
df_rating=df_rating[['nation','overall','attack','mid','defence']]
for i in range(len(df_rating["nation"])):
    df_rating["nation"][i]=df_rating["nation"][i].replace("Côte d'Ivoire", "Ivory Coast")
    df_rating["nation"][i]=df_rating["nation"][i].replace("Korea Republic", "South Korea")
    
Countary=list(df_rating['nation'].unique())
Countary.sort()

# print(Countary)
# print(len(Countary))

#Groupby different and average the rating
df_rating_group=df_rating.groupby(['nation']).agg(['mean'])
#Rating 縮減到小數後兩位
df_rating_group=df_rating_group.applymap(lambda x: '%.2f'%x)
# print(df_rating_group)

#%%
#List all country name(df_rating)
nation_set=set(nation_name)
Countary_set=set(Countary)

#Check missing countary
# print(nation_set-Countary_set)
# print('-'*100)
# print(Countary_set-nation_set)

#%%
#Insert team rating data to df_OddAndResult

ovr_home=[]
att_home=[]
mid_home=[]
defe_home=[]

ovr_away=[]
att_away=[]
mid_away=[]
defe_away=[]

Insert_column=[ovr_home,att_home,mid_home,defe_home,
                ovr_away,att_away,mid_away,defe_away]
Insert_title=['ovr_home','att_home','mid_home','defe_home',
                'ovr_away','att_away','mid_away','defe_away']

#Check nation different (Na value in list)
# df_OddAndResult.insert(11,'if_match','N')

for i in range(len(df_OddAndResult)):
    for j in range(len(df_rating_group)):
        if df_OddAndResult['home_team'][i]==df_rating_group.index[j]:
            ovr_home.append(df_rating_group['overall']['mean'][j])
            att_home.append(df_rating_group['attack']['mean'][j])
            mid_home.append(df_rating_group['mid']['mean'][j])
            defe_home.append(df_rating_group['defence']['mean'][j])
            # df_OddAndResult['if_match'][i]='Y'
        if df_OddAndResult['away_team'][i]==df_rating_group.index[j]:
            ovr_away.append(df_rating_group['overall']['mean'][j])
            att_away.append(df_rating_group['attack']['mean'][j])
            mid_away.append(df_rating_group['mid']['mean'][j])
            defe_away.append(df_rating_group['defence']['mean'][j])
            # df_OddAndResult['if_match'][i]='Y'
            
# print(df_OddAndResult[df_OddAndResult['if_match']=='N'])
            
for k in range(8):
    df_OddAndResult.insert(k+10,Insert_title[k],Insert_column[k])
    df_OddAndResult[Insert_title[k]]=df_OddAndResult[Insert_title[k]].astype('float64')
print(df_OddAndResult.info())


#%%
# df_OddAndResult.to_csv("OddCombineRating.csv", index = None)
            
#%%
#Import team ranking & Country_code
df_ranking = pd.read_csv('AllTime_ranking.csv')
df_country_code = pd.read_csv('Country_code.csv')
# print(df_ranking.info())
# print(df_country_code.info())

#Replace contary_code as full country name in df_ranking
df_ranking_merge = df_ranking.merge(df_country_code, how='inner', indicator=False)
df_ranking_merge=df_ranking_merge[['Country','Year','Previous_Rank','Total_Points','Country_Code']]
print(df_ranking_merge.info())

#Check missing data
# df_ranking_out = df_ranking.merge(df_country_code, how='outer', 
#                                   indicator=True).loc[lambda x : x['_merge'] == 'left_only']
# print(df_ranking_out)

#%%
#Insert team ranking data to df_OddAndResult
Previous_Rank_home=[]
Total_Points_home=[]
Country_Code_home=[]

Previous_Rank_away=[]
Total_Points_away=[]
Country_Code_away=[]

insert_items=[Previous_Rank_home,Total_Points_home,Country_Code_home,
              Previous_Rank_away,Total_Points_away,Country_Code_away]
insert_items_title=['Previous_Rank_home','Total_Points_home','Country_Code_home',
                    'Previous_Rank_away','Total_Points_away','Country_Code_away']

for i in range(len(df_OddAndResult)):
    for j in range(len(df_ranking_merge)):
        if df_OddAndResult['home_team'][i]==df_ranking_merge['Country'][j] and df_OddAndResult['date'][i]==df_ranking_merge['Year'][j]:
            Previous_Rank_home.append(df_ranking_merge['Previous_Rank'][j])
            Total_Points_home.append(df_ranking_merge['Total_Points'][j])
            Country_Code_home.append(df_ranking_merge['Country_Code'][j])
        if df_OddAndResult['away_team'][i]==df_ranking_merge['Country'][j] and df_OddAndResult['date'][i]==df_ranking_merge['Year'][j]:
            Previous_Rank_away.append(df_ranking_merge['Previous_Rank'][j])
            Total_Points_away.append(df_ranking_merge['Total_Points'][j])
            Country_Code_away.append(df_ranking_merge['Country_Code'][j])
            
for k in range(len(insert_items)):
    df_OddAndResult.insert(k+18,insert_items_title[k],insert_items[k])
    if k==0 or k==1 or k==3 or k==4:
        df_OddAndResult[insert_items_title[k]]=df_OddAndResult[insert_items_title[k]].astype('float64')
# print(df_OddAndResult.info())

#%%
#Add columns for ovr/rank/points difference

ovr_difference=[]
att_difference=[]
mid_difference=[]
defe_difference=[]

rank_difference=[]
point_difference=[]

for i in range(len(df_OddAndResult)):
    ovr_dif=df_OddAndResult['ovr_home'][i]-df_OddAndResult['ovr_away'][i]
    ovr_difference.append(ovr_dif)
    att_dif=df_OddAndResult['att_home'][i]-df_OddAndResult['att_away'][i]
    att_difference.append(att_dif)
    mid_dif=df_OddAndResult['mid_home'][i]-df_OddAndResult['mid_away'][i]
    mid_difference.append(mid_dif)
    defe_dif=df_OddAndResult['defe_home'][i]-df_OddAndResult['defe_away'][i]
    defe_difference.append(defe_dif)
    rank_dif=df_OddAndResult['Previous_Rank_home'][i]-df_OddAndResult['Previous_Rank_away'][i]
    rank_difference.append(rank_dif)
    point_dif=df_OddAndResult['Total_Points_home'][i]-df_OddAndResult['Total_Points_away'][i]
    point_difference.append(point_dif)


df_OddAndResult.insert(25,'ovr_dif',ovr_difference)
df_OddAndResult.insert(26,'att_dif',att_difference)
df_OddAndResult.insert(27,'mid_dif',mid_difference)
df_OddAndResult.insert(28,'defe_dif',defe_difference)
df_OddAndResult.insert(29,'rank_dif',rank_difference)
df_OddAndResult.insert(30,'points_dif',point_difference)
print(df_OddAndResult.info())

#%%
#Import Elo_rating data

df_RloRating = pd.read_csv('Elo_cleanData.csv')
#Nation_name in RloRating
Rlo_nation=df_RloRating['Country_simp'].unique()

# print(sorted(Rlo_nation))
# print(df_RloRating.info())

#%%
#Inser Elo_rating data to df_OddAndResult

Elo_ranking_home=[]
Elo_rating_home=[]
total_game_home=[]
total_wins_home=[]
total_draw_home=[]
total_lose_home=[]
goal_for_home=[]
goal_against_home=[]

Elo_ranking_away=[]
Elo_rating_away=[]
total_game_away=[]
total_wins_away=[]
total_draw_away=[]
total_lose_away=[]
goal_for_away=[]
goal_against_away=[]

Insert_Elo_column=[Elo_ranking_home,Elo_rating_home,total_game_home,total_wins_home,total_draw_home,total_lose_home,
                    goal_for_home,goal_against_home,Elo_ranking_away,Elo_rating_away,
                    total_game_away,total_wins_away,total_draw_away,total_lose_away,goal_for_away,goal_against_away]
Insert_Elo_title=['Elo_ranking_home','Elo_rating_home','total_game_home',
                  'total_wins_home','total_draw_home','total_lose_home','goal_for_home','goal_against_home',
                  'Elo_ranking_away','Elo_rating_away','total_game_away',
                  'total_wins_away','total_draw_away','total_lose_away','goal_for_away','goal_against_away']

#Check nation name different
# df_OddAndResult.insert(29,'if_match','N')

for i in range(len(df_OddAndResult)):
    for j in range(len(df_RloRating)):
        if df_OddAndResult['home_team'][i]==df_RloRating['Country_simp'][j] and df_OddAndResult['date'][i]==df_RloRating['year'][j]:
            Elo_ranking_home.append(df_RloRating['Elo_ranking'][j])
            Elo_rating_home.append(df_RloRating['Elo_rating'][j])
            total_game_home.append(df_RloRating['total_game'][j])
            total_wins_home.append(df_RloRating['total_wins'][j])
            total_draw_home.append(df_RloRating['total_draw'][j])
            total_lose_home.append(df_RloRating['total_lose'][j])
            goal_for_home.append(df_RloRating['goal_for'][j])
            goal_against_home.append(df_RloRating['goal_against'][j])
            # df_OddAndResult['if_match'][i]='Y'
        if df_OddAndResult['away_team'][i]==df_RloRating['Country_simp'][j] and df_OddAndResult['date'][i]==df_RloRating['year'][j]:
            Elo_ranking_away.append(df_RloRating['Elo_ranking'][j])
            Elo_rating_away.append(df_RloRating['Elo_rating'][j])
            total_game_away.append(df_RloRating['total_game'][j])
            total_wins_away.append(df_RloRating['total_wins'][j])
            total_draw_away.append(df_RloRating['total_draw'][j])
            total_lose_away.append(df_RloRating['total_lose'][j])
            goal_for_away.append(df_RloRating['goal_for'][j])
            goal_against_away.append(df_RloRating['goal_against'][j])
            # df_OddAndResult['if_match'][i]='Y'

#Check nation name different
# print(len(df_OddAndResult))
# print(len(Elo_ranking_home))
# print(len(Elo_ranking_away))
# print(df_OddAndResult[df_OddAndResult['if_match']=='N'])

# print(len(Insert_Elo_title))
# print(len(Insert_Elo_column))
# print(len(Elo_ranking_home))
# print(len(Elo_ranking_away))

for k in range(len(Insert_Elo_title)):
    df_OddAndResult.insert(k+30,Insert_Elo_title[k],Insert_Elo_column[k])
    
# print(df_OddAndResult.info())

#%%
#Add columns for win_rate/draw_rate_home/lose_rate_home/goal_balance

win_rate_home=[]
draw_rate_home=[]
lose_rate_home=[]
goal_balance_home=[]

win_rate_away=[]
draw_rate_away=[]
lose_rate_away=[]
goal_balance_away=[]

for i in range(len(df_OddAndResult)):
    wins_rate_home=df_OddAndResult['total_wins_home'][i]/df_OddAndResult['total_game_home'][i]*100
    win_rate_home.append(wins_rate_home)
    draws_rate_home=df_OddAndResult['total_draw_home'][i]/df_OddAndResult['total_game_home'][i]*100
    draw_rate_home.append(draws_rate_home)
    lossing_rate_home=df_OddAndResult['total_lose_home'][i]/df_OddAndResult['total_game_home'][i]*100
    lose_rate_home.append(lossing_rate_home)
    goals_balance_home=(df_OddAndResult['goal_for_home'][i]-df_OddAndResult['goal_against_home'][i])/df_OddAndResult['total_game_home'][i]
    goal_balance_home.append(goals_balance_home)
    
    wins_rate_away=df_OddAndResult['total_wins_away'][i]/df_OddAndResult['total_game_away'][i]*100
    win_rate_away.append(wins_rate_away)
    draws_rate_away=df_OddAndResult['total_draw_away'][i]/df_OddAndResult['total_game_away'][i]*100
    draw_rate_away.append(draws_rate_away)
    lossing_rate_away=df_OddAndResult['total_lose_away'][i]/df_OddAndResult['total_game_away'][i]*100
    lose_rate_away.append(lossing_rate_away)
    goals_balance_away=(df_OddAndResult['goal_for_away'][i]-df_OddAndResult['goal_against_away'][i])/df_OddAndResult['total_game_away'][i]
    goal_balance_away.append(goals_balance_away)
    
df_OddAndResult.insert(47,'win_rate_home',win_rate_home)
df_OddAndResult.insert(48,'draw_rate_home',draw_rate_home)
df_OddAndResult.insert(49,'lose_rate_home',lose_rate_home)
df_OddAndResult.insert(50,'goal_balance_home',goal_balance_home)
df_OddAndResult.insert(51,'win_rate_away',win_rate_away)
df_OddAndResult.insert(52,'draw_rate_away',draw_rate_away)
df_OddAndResult.insert(53,'lose_rate_away',lose_rate_away)
df_OddAndResult.insert(54,'goal_balance_away',goal_balance_away)
# print(df_OddAndResult.info())

#%%
#Add columns for Elo_ranking/Elo_rating/win_rate/draw_rate/lose_rate/goal_balance/goal_for/goal_against difference

Elo_ranking_difference=[]
Elo_rating_difference=[]
win_rate_difference=[]
draw_rate_difference=[]
lose_rate_difference=[]
goal_balance_difference=[]
goal_for_difference=[]
goal_against_difference=[]

for i in range(len(df_OddAndResult)):
    Elo_ranking_dif=df_OddAndResult['Elo_ranking_home'][i]-df_OddAndResult['Elo_ranking_away'][i]
    Elo_ranking_difference.append(Elo_ranking_dif)
    Elo_rating_dif=df_OddAndResult['Elo_rating_home'][i]-df_OddAndResult['Elo_rating_away'][i]
    Elo_rating_difference.append(Elo_rating_dif)
    win_rate_dif=df_OddAndResult['win_rate_home'][i]-df_OddAndResult['win_rate_away'][i]
    win_rate_difference.append(win_rate_dif)
    draw_rate_dif=df_OddAndResult['win_rate_home'][i]-df_OddAndResult['win_rate_away'][i]
    draw_rate_difference.append(draw_rate_dif)
    lose_rate_dif=df_OddAndResult['win_rate_home'][i]-df_OddAndResult['win_rate_away'][i]
    lose_rate_difference.append(lose_rate_dif)
    goal_balance_dif=df_OddAndResult['goal_balance_home'][i]-df_OddAndResult['goal_balance_away'][i]
    goal_balance_difference.append(goal_balance_dif)
    goal_for_dif=df_OddAndResult['goal_balance_home'][i]-df_OddAndResult['goal_balance_away'][i]
    goal_for_difference.append(goal_for_dif)
    goal_against_dif=df_OddAndResult['goal_balance_home'][i]-df_OddAndResult['goal_balance_away'][i]
    goal_against_difference.append(goal_against_dif)


df_OddAndResult.insert(55,'Elo_ranking_dif',Elo_ranking_difference)
df_OddAndResult.insert(56,'Elo_rating_dif',Elo_rating_difference)
df_OddAndResult.insert(57,'win_rate_dif',win_rate_difference)
df_OddAndResult.insert(58,'draw_rate_dif',draw_rate_difference)
df_OddAndResult.insert(59,'lose_rate_dif',lose_rate_difference)
df_OddAndResult.insert(60,'goal_balance_dif',goal_balance_difference)
df_OddAndResult.insert(61,'goal_for_dif',goal_for_difference)
df_OddAndResult.insert(62,'goal_against_dif',goal_against_difference)
print(df_OddAndResult.info())


#%%
df_OddAndResult.to_csv("cleanData_V3.csv", index = None)


