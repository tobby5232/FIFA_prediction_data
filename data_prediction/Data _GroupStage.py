# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 22:40:09 2022

@author: ch406
"""

import pandas as pd

#%%
#Import all comptition result
df_result = pd.read_csv('results.csv')

#Simplifized date formate to year only
for i in range(len(df_result["date"])):
    df_result["date"][i]=df_result["date"][i][:4]
df_result["date"]=df_result["date"].astype(int)
year=df_result['date'].unique()

#Simplifized dataFrame only world cup betewwn 2006~2018
df_result=df_result[(df_result['date'] >=2022) & (df_result['tournament']=='FIFA World Cup')]
df_result=df_result[['date','home_team','away_team']]

df_group_stage=df_result.head(48)
df_group_stage=df_group_stage.reset_index(drop=True)

# print(df_group_stage)

#%%
#Import team rating

df_rating = pd.read_csv('AllTeamRating.csv')
df_rating=df_rating[['nation','overall','attack','mid','defence']]
for i in range(len(df_rating["nation"])):
    df_rating["nation"][i]=df_rating["nation"][i].replace("Côte d'Ivoire", "Ivory Coast")
    df_rating["nation"][i]=df_rating["nation"][i].replace("Korea Republic", "South Korea")
    
Countary=list(df_rating['nation'].unique())
Countary.sort()

#Groupby different and average the rating
df_rating_group=df_rating.groupby(['nation']).agg(['mean'])
#Rating 縮減到小數後兩位
df_rating_group=df_rating_group.applymap(lambda x: '%.2f'%x)
print(df_rating_group.info())

#%%
#Insert team rating data to df_group_stage

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
# df_group_stage.insert(11,'if_match','N')

for i in range(len(df_group_stage)):
    for j in range(len(df_rating_group)):
        if df_group_stage['home_team'][i]==df_rating_group.index[j]:
            ovr_home.append(df_rating_group['overall']['mean'][j])
            att_home.append(df_rating_group['attack']['mean'][j])
            mid_home.append(df_rating_group['mid']['mean'][j])
            defe_home.append(df_rating_group['defence']['mean'][j])
            # df_group_stage['if_match'][i]='Y'
        if df_group_stage['away_team'][i]==df_rating_group.index[j]:
            ovr_away.append(df_rating_group['overall']['mean'][j])
            att_away.append(df_rating_group['attack']['mean'][j])
            mid_away.append(df_rating_group['mid']['mean'][j])
            defe_away.append(df_rating_group['defence']['mean'][j])
            # df_group_stage['if_match'][i]='Y'
            
# print(df_group_stage[df_group_stage['if_match']=='N'])
            
for k in range(8):
    df_group_stage.insert(len(df_group_stage.columns),Insert_title[k],Insert_column[k])
    df_group_stage[Insert_title[k]]=df_group_stage[Insert_title[k]].astype('float64')
print(df_group_stage.info())
            
#%%
#Import team ranking & Country_code
df_ranking = pd.read_csv('AllTime_ranking.csv')
df_country_code = pd.read_csv('Country_code.csv')

#Replace contary_code as full country name in df_ranking
df_ranking_merge = df_ranking.merge(df_country_code, how='inner', indicator=False)
df_ranking_merge=df_ranking_merge[['Country','Year','Previous_Rank','Total_Points','Country_Code']]
# print(df_ranking_merge.info())

#Check missing data
# df_ranking_out = df_ranking.merge(df_country_code, how='outer', 
#                                   indicator=True).loc[lambda x : x['_merge'] == 'left_only']
# print(df_ranking_out)

#%%
#Insert team ranking data to df_group_stage
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

for i in range(len(df_group_stage)):
    for j in range(len(df_ranking_merge)):
        if df_group_stage['home_team'][i]==df_ranking_merge['Country'][j] and df_group_stage['date'][i]==df_ranking_merge['Year'][j]:
            Previous_Rank_home.append(df_ranking_merge['Previous_Rank'][j])
            Total_Points_home.append(df_ranking_merge['Total_Points'][j])
            Country_Code_home.append(df_ranking_merge['Country_Code'][j])
        if df_group_stage['away_team'][i]==df_ranking_merge['Country'][j] and df_group_stage['date'][i]==df_ranking_merge['Year'][j]:
            Previous_Rank_away.append(df_ranking_merge['Previous_Rank'][j])
            Total_Points_away.append(df_ranking_merge['Total_Points'][j])
            Country_Code_away.append(df_ranking_merge['Country_Code'][j])
            
for k in range(len(insert_items)):
    df_group_stage.insert(len(df_group_stage.columns),insert_items_title[k],insert_items[k])
# print(df_group_stage.info())

#%%
#Add columns for ovr/rank/points difference

ovr_difference=[]
att_difference=[]
mid_difference=[]
defe_difference=[]

rank_difference=[]
point_difference=[]

for i in range(len(df_group_stage)):
    ovr_dif=df_group_stage['ovr_home'][i]-df_group_stage['ovr_away'][i]
    ovr_difference.append(ovr_dif)
    att_dif=df_group_stage['att_home'][i]-df_group_stage['att_away'][i]
    att_difference.append(att_dif)
    mid_dif=df_group_stage['mid_home'][i]-df_group_stage['mid_away'][i]
    mid_difference.append(mid_dif)
    defe_dif=df_group_stage['defe_home'][i]-df_group_stage['defe_away'][i]
    defe_difference.append(defe_dif)
    rank_dif=df_group_stage['Previous_Rank_home'][i]-df_group_stage['Previous_Rank_away'][i]
    rank_difference.append(rank_dif)
    point_dif=df_group_stage['Total_Points_home'][i]-df_group_stage['Total_Points_away'][i]
    point_difference.append(point_dif)


df_group_stage.insert(17,'ovr_dif',ovr_difference)
df_group_stage.insert(18,'att_dif',att_difference)
df_group_stage.insert(19,'mid_dif',mid_difference)
df_group_stage.insert(20,'defe_dif',defe_difference)
df_group_stage.insert(21,'rank_dif',rank_difference)
df_group_stage.insert(22,'points_dif',point_difference)
# print(df_group_stage.info())

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
# df_group_stage.insert(29,'if_match','N')

for i in range(len(df_group_stage)):
    for j in range(len(df_RloRating)):
        if df_group_stage['home_team'][i]==df_RloRating['Country_simp'][j] and df_group_stage['date'][i]==df_RloRating['year'][j]:
            Elo_ranking_home.append(df_RloRating['Elo_ranking'][j])
            Elo_rating_home.append(df_RloRating['Elo_rating'][j])
            total_game_home.append(df_RloRating['total_game'][j])
            total_wins_home.append(df_RloRating['total_wins'][j])
            total_draw_home.append(df_RloRating['total_draw'][j])
            total_lose_home.append(df_RloRating['total_lose'][j])
            goal_for_home.append(df_RloRating['goal_for'][j])
            goal_against_home.append(df_RloRating['goal_against'][j])
            # df_group_stage['if_match'][i]='Y'
        if df_group_stage['away_team'][i]==df_RloRating['Country_simp'][j] and df_group_stage['date'][i]==df_RloRating['year'][j]:
            Elo_ranking_away.append(df_RloRating['Elo_ranking'][j])
            Elo_rating_away.append(df_RloRating['Elo_rating'][j])
            total_game_away.append(df_RloRating['total_game'][j])
            total_wins_away.append(df_RloRating['total_wins'][j])
            total_draw_away.append(df_RloRating['total_draw'][j])
            total_lose_away.append(df_RloRating['total_lose'][j])
            goal_for_away.append(df_RloRating['goal_for'][j])
            goal_against_away.append(df_RloRating['goal_against'][j])
            # df_group_stage['if_match'][i]='Y'

#Check nation name different
# print(len(df_group_stage))
# print(len(Elo_ranking_home))
# print(len(Elo_ranking_away))
# print(df_group_stage[df_group_stage['if_match']=='N'])

# print(len(Insert_Elo_title))
# print(len(Insert_Elo_column))
# print(len(Elo_ranking_home))
# print(len(Elo_ranking_away))

for k in range(len(Insert_Elo_title)):
    df_group_stage.insert(len(df_group_stage.columns),Insert_Elo_title[k],Insert_Elo_column[k])
    
# print(df_group_stage.info())

#%%
#Add columns for Elo_ranking/Elo_rating difference

Elo_ranking_difference=[]
Elo_rating_difference=[]

for i in range(len(df_group_stage)):
    Elo_ranking_dif=df_group_stage['Elo_ranking_home'][i]-df_group_stage['Elo_ranking_away'][i]
    Elo_ranking_difference.append(Elo_ranking_dif)
    Elo_rating_dif=df_group_stage['Elo_rating_home'][i]-df_group_stage['Elo_rating_away'][i]
    Elo_rating_difference.append(Elo_rating_dif)

df_group_stage.insert(39,'Elo_ranking_dif',Elo_ranking_difference)
df_group_stage.insert(40,'Elo_rating_dif',Elo_rating_difference)
# print(df_group_stage.info())

#%%
#Simplized data
df_group_stage=df_group_stage[['home_team','away_team',
                               'ovr_home','ovr_away',
                               'ovr_dif',
                               'att_home','att_away',
                               'att_dif',
                               'mid_home','mid_away',
                               'mid_dif',
                               'defe_home','defe_away',
                               'defe_dif',
                               'Previous_Rank_home','Previous_Rank_away',
                               'rank_dif',
                               'Total_Points_home','Total_Points_away',
                               'points_dif',
                               'Elo_ranking_home','Elo_ranking_away',
                               'Elo_ranking_dif',
                               'Elo_rating_home','Elo_rating_away',
                               'Elo_rating_dif',]]
print(df_group_stage.info())

#%%
df_group_stage.to_csv("data_group_stage.csv", index = None)