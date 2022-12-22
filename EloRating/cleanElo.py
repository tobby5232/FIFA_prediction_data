# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 16:39:30 2022

@author: ch406
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re
import numpy as np


#%%
# Import 2006 data
df_2006_rating = pd.read_csv('2006.tsv',sep='\t')

#Select necessary data
colunm=['Elo_ranking','Country_simp','Elo_rating','avg_rank','avg_rating','total_game',
        'total_wins','total_lose','total_draw','goal_for','goal_against']

df_2006_rating.loc[-1]=df_2006_rating.columns
df_2006_rating=df_2006_rating.iloc[:,[1,2,3,6,7,22,26,27,28,29,30]]
df_2006_rating.columns=colunm

df_2006_rating=df_2006_rating.astype({'Elo_ranking': 'int32',
                                      'Elo_rating': 'int32',
                                      'avg_rank': 'int32',
                                      'avg_rating': 'int32',
                                      'total_game': 'int32',
                                      'total_wins': 'int32',
                                      'total_lose': 'int32',
                                      'total_draw': 'int32',
                                      'goal_for': 'int32',
                                      'goal_against': 'int32'})
df_2006_rating=df_2006_rating.sort_values(by=['Elo_ranking'])
df_2006_rating=df_2006_rating.reset_index(drop=True)
df_2006_rating.insert(11,'year',2006)

# print(df_2006_rating[df_2006_rating.isnull().values==True])
df_2006_rating['Country_simp'].fillna(value='Not Namibia', inplace=True)
print(df_2006_rating.head())
print(df_2006_rating.info())

#%%
# Import 2008 data
df_2008_rating = pd.read_csv('2008.tsv',sep='\t')

#Select necessary data
colunm=['Elo_ranking','Country_simp','Elo_rating','avg_rank','avg_rating','total_game',
        'total_wins','total_lose','total_draw','goal_for','goal_against']

df_2008_rating.loc[-1]=df_2008_rating.columns
df_2008_rating=df_2008_rating.iloc[:,[1,2,3,6,7,22,26,27,28,29,30]]
df_2008_rating.columns=colunm

df_2008_rating=df_2008_rating.astype({'Elo_ranking': 'int32',
                                      'Elo_rating': 'int32',
                                      'avg_rank': 'int32',
                                      'avg_rating': 'int32',
                                      'total_game': 'int32',
                                      'total_wins': 'int32',
                                      'total_lose': 'int32',
                                      'total_draw': 'int32',
                                      'goal_for': 'int32',
                                      'goal_against': 'int32'})
df_2008_rating=df_2008_rating.sort_values(by=['Elo_ranking'])
df_2008_rating=df_2008_rating.reset_index(drop=True)
df_2008_rating.insert(11,'year',2008)

# print(df_2008_rating[df_2008_rating.isnull().values==True])
df_2008_rating['Country_simp'].fillna(value='Not Namibia', inplace=True)
print(df_2008_rating.head())
print(df_2008_rating.info())

#%%
# Import 2010 data
df_2010_rating = pd.read_csv('2010.tsv',sep='\t')

#Select necessary data
colunm=['Elo_ranking','Country_simp','Elo_rating','avg_rank','avg_rating','total_game',
        'total_wins','total_lose','total_draw','goal_for','goal_against']

df_2010_rating.loc[-1]=df_2010_rating.columns
df_2010_rating=df_2010_rating.iloc[:,[1,2,3,6,7,22,26,27,28,29,30]]
df_2010_rating.columns=colunm

df_2010_rating=df_2010_rating.astype({'Elo_ranking': 'int32',
                                      'Elo_rating': 'int32',
                                      'avg_rank': 'int32',
                                      'avg_rating': 'int32',
                                      'total_game': 'int32',
                                      'total_wins': 'int32',
                                      'total_lose': 'int32',
                                      'total_draw': 'int32',
                                      'goal_for': 'int32',
                                      'goal_against': 'int32'})
df_2010_rating=df_2010_rating.sort_values(by=['Elo_ranking'])
df_2010_rating=df_2010_rating.reset_index(drop=True)
df_2010_rating.insert(11,'year',2010)

# print(df_2010_rating[df_2010_rating.isnull().values==True])
df_2010_rating['Country_simp'].fillna(value='Not Namibia', inplace=True)
print(df_2010_rating.head())
print(df_2010_rating.info())

#%%
# Import 2012 data
df_2012_rating = pd.read_csv('2012.tsv',sep='\t')

#Select necessary data
colunm=['Elo_ranking','Country_simp','Elo_rating','avg_rank','avg_rating','total_game',
        'total_wins','total_lose','total_draw','goal_for','goal_against']

df_2012_rating.loc[-1]=df_2012_rating.columns
df_2012_rating=df_2012_rating.iloc[:,[1,2,3,6,7,22,26,27,28,29,30]]
df_2012_rating.columns=colunm

df_2012_rating=df_2012_rating.astype({'Elo_ranking': 'int32',
                                      'Elo_rating': 'int32',
                                      'avg_rank': 'int32',
                                      'avg_rating': 'int32',
                                      'total_game': 'int32',
                                      'total_wins': 'int32',
                                      'total_lose': 'int32',
                                      'total_draw': 'int32',
                                      'goal_for': 'int32',
                                      'goal_against': 'int32'})
df_2012_rating=df_2012_rating.sort_values(by=['Elo_ranking'])
df_2012_rating=df_2012_rating.reset_index(drop=True)
df_2012_rating.insert(11,'year',2012)

# print(df_2012_rating[df_2012_rating.isnull().values==True])
df_2012_rating['Country_simp'].fillna(value='Not Namibia', inplace=True)
print(df_2012_rating.head())
print(df_2012_rating.info())

#%%
# Import 2014 data
df_2014_rating = pd.read_csv('2014.tsv',sep='\t')

#Select necessary data
colunm=['Elo_ranking','Country_simp','Elo_rating','avg_rank','avg_rating','total_game',
        'total_wins','total_lose','total_draw','goal_for','goal_against']

df_2014_rating.loc[-1]=df_2014_rating.columns
df_2014_rating=df_2014_rating.iloc[:,[1,2,3,6,7,22,26,27,28,29,30]]
df_2014_rating.columns=colunm

df_2014_rating=df_2014_rating.astype({'Elo_ranking': 'int32',
                                      'Elo_rating': 'int32',
                                      'avg_rank': 'int32',
                                      'avg_rating': 'int32',
                                      'total_game': 'int32',
                                      'total_wins': 'int32',
                                      'total_lose': 'int32',
                                      'total_draw': 'int32',
                                      'goal_for': 'int32',
                                      'goal_against': 'int32'})
df_2014_rating=df_2014_rating.sort_values(by=['Elo_ranking'])
df_2014_rating=df_2014_rating.reset_index(drop=True)
df_2014_rating.insert(11,'year',2014)

# print(df_2014_rating[df_2014_rating.isnull().values==True])
df_2014_rating['Country_simp'].fillna(value='Not Namibia', inplace=True)
print(df_2014_rating.head())
print(df_2014_rating.info())

#%%
# Import 2016 data
df_2016_rating = pd.read_csv('2016.tsv',sep='\t')

#Select necessary data
colunm=['Elo_ranking','Country_simp','Elo_rating','avg_rank','avg_rating','total_game',
        'total_wins','total_lose','total_draw','goal_for','goal_against']

df_2016_rating.loc[-1]=df_2016_rating.columns
df_2016_rating=df_2016_rating.iloc[:,[1,2,3,6,7,22,26,27,28,29,30]]
df_2016_rating.columns=colunm

df_2016_rating=df_2016_rating.astype({'Elo_ranking': 'int32',
                                      'Elo_rating': 'int32',
                                      'avg_rank': 'int32',
                                      'avg_rating': 'int32',
                                      'total_game': 'int32',
                                      'total_wins': 'int32',
                                      'total_lose': 'int32',
                                      'total_draw': 'int32',
                                      'goal_for': 'int32',
                                      'goal_against': 'int32'})
df_2016_rating=df_2016_rating.sort_values(by=['Elo_ranking'])
df_2016_rating=df_2016_rating.reset_index(drop=True)
df_2016_rating.insert(11,'year',2016)

# print(df_2016_rating[df_2016_rating.isnull().values==True])
df_2016_rating['Country_simp'].fillna(value='Not Namibia', inplace=True)
print(df_2016_rating.head())
print(df_2016_rating.info())

#%%
# Import 2018 data
df_2018_rating = pd.read_csv('2018.tsv',sep='\t')

#Select necessary data
colunm=['Elo_ranking','Country_simp','Elo_rating','avg_rank','avg_rating','total_game',
        'total_wins','total_lose','total_draw','goal_for','goal_against']

df_2018_rating.loc[-1]=df_2018_rating.columns
df_2018_rating=df_2018_rating.iloc[:,[1,2,3,6,7,22,26,27,28,29,30]]
df_2018_rating.columns=colunm

df_2018_rating=df_2018_rating.astype({'Elo_ranking': 'int32',
                                      'Elo_rating': 'int32',
                                      'avg_rank': 'int32',
                                      'avg_rating': 'int32',
                                      'total_game': 'int32',
                                      'total_wins': 'int32',
                                      'total_lose': 'int32',
                                      'total_draw': 'int32',
                                      'goal_for': 'int32',
                                      'goal_against': 'int32'})
df_2018_rating=df_2018_rating.sort_values(by=['Elo_ranking'])
df_2018_rating=df_2018_rating.reset_index(drop=True)
df_2018_rating.insert(11,'year',2018)

# print(df_2018_rating[df_2018_rating.isnull().values==True])
df_2018_rating['Country_simp'].fillna(value='Not Namibia', inplace=True)
print(df_2018_rating.head())
print(df_2018_rating.info())

#%%
# Import 2021 data
df_2021_rating = pd.read_csv('2021.tsv',sep='\t')

#Select necessary data
colunm=['Elo_ranking','Country_simp','Elo_rating','avg_rank','avg_rating','total_game',
        'total_wins','total_lose','total_draw','goal_for','goal_against']

df_2021_rating.loc[-1]=df_2021_rating.columns
df_2021_rating=df_2021_rating.iloc[:,[1,2,3,6,7,22,26,27,28,29,30]]
df_2021_rating.columns=colunm

df_2021_rating=df_2021_rating.astype({'Elo_ranking': 'int32',
                                      'Elo_rating': 'int32',
                                      'avg_rank': 'int32',
                                      'avg_rating': 'int32',
                                      'total_game': 'int32',
                                      'total_wins': 'int32',
                                      'total_lose': 'int32',
                                      'total_draw': 'int32',
                                      'goal_for': 'int32',
                                      'goal_against': 'int32'})
df_2021_rating=df_2021_rating.sort_values(by=['Elo_ranking'])
df_2021_rating=df_2021_rating.reset_index(drop=True)
df_2021_rating.insert(11,'year',2021)

# print(df_2021_rating[df_2021_rating.isnull().values==True])
df_2021_rating['Country_simp'].fillna(value='Not Namibia', inplace=True)
print(df_2021_rating.head())
print(df_2021_rating.info())

#%%
# Import 2022 data
df_2022_rating = pd.read_csv('2022.tsv',sep='\t')

#Select necessary data
colunm=['Elo_ranking','Country_simp','Elo_rating','avg_rank','avg_rating','total_game',
        'total_wins','total_lose','total_draw','goal_for','goal_against']

df_2022_rating.loc[-1]=df_2022_rating.columns
df_2022_rating=df_2022_rating.iloc[:,[1,2,3,6,7,22,26,27,28,29,30]]
df_2022_rating.columns=colunm

df_2022_rating=df_2022_rating.astype({'Elo_ranking': 'int32',
                                      'Elo_rating': 'int32',
                                      'avg_rank': 'int32',
                                      'avg_rating': 'int32',
                                      'total_game': 'int32',
                                      'total_wins': 'int32',
                                      'total_lose': 'int32',
                                      'total_draw': 'int32',
                                      'goal_for': 'int32',
                                      'goal_against': 'int32'})
df_2022_rating=df_2022_rating.sort_values(by=['Elo_ranking'])
df_2022_rating=df_2022_rating.reset_index(drop=True)
df_2022_rating.insert(11,'year',2022)

# print(df_2022_rating[df_2022_rating.isnull().values==True])
df_2022_rating['Country_simp'].fillna(value='Not Namibia', inplace=True)
print(df_2022_rating.head())
print(df_2022_rating.info())

#%%
#Concate all data

newData=pd.concat([df_2006_rating,df_2008_rating,df_2010_rating,df_2012_rating,df_2014_rating,
                   df_2016_rating,df_2018_rating,df_2021_rating,df_2022_rating])

print(newData.info())

#%%
#Replace country simple name as full name
Country_simp = df_2022_rating['Country_simp'].values.tolist()
Country_simp.append('SZ')
Country_simp.append('MK')
Country_simp.append('AN')
Country_full=['Argentina','Brazil','France','Netherlands','Portugal','Spain','Italy','England',
              'Germany','Croatia','Belgium','Colombia','Uruguay','Denmark','Switzerland',
              'Morocco','Peru','Japan','Ecuador','Serbia','Hungary','Ukraine','United States','Mexico','Poland',
              'South Korea','Czech Republic','Iran','Australia','Sweden','Norway','Russia','Scotland','Austria',
              'Tunisia','Senegal','Costa Rica','Paraguay','Wales','Turkey','Canada','Algeria','Chile','Greece',
              'Finland','Venezuela','Cameroon','Republic of Ireland','Ivory Coast','Slovenia','Egypt','Georgia','Panama',
              'Saudi Arabia','Nigeria','Mali','Israel','Bolivia','Bosnia and Herzegovina','Romania','Burkina Faso',
              'Ghana','Jordan','Slovakia','Qatar','Uzbekistan','Iraq','Jamaica','Oman','South Africa','Iceland',
              'Albania','Montenegro','Northern Ireland','Haiti','North Macedonia','New Zealand','Bulgaria','Kosovo',
              'Bahrain','Gabon','UAE','Cape Verde','El Salvador','Honduras','China','Zambia','DR Congo',
              'North Cyprus','Armenia','Guatemala','Luxembourg','Equat Guinea','Palestine','Estonia','Kurdistan',
              'Syria','Gambia','Azerbaijan','Belarus','Angola','Uganda','Vietnam','Benin','Mauritania','Kazakhstan',
              'Martinique','Guinea','Guinea-Bissau','North Korea','Kenya','Thailand','Namibia','Réunion',
              'Curaçao','Botswana','Cyprus','Libya','Latvia','Ethiopia','French Guiana','Trinidad and Tobago',
              'Sierra Leone','Zanzibar','Cuba','Tajikistan','Mozambique','Suriname','Lebanon','Togo','Zimbabwe',
              'Kuwait','Tanzania','Liberia','Faroe Islands','Sudan','Madagascar','Congo','Eswatini','Malawi',
              'Rwanda','Indonesia','C African Rep','Kyrgyzstan','Malta','Nicaragua','Burundi','Turkmenistan',
              'Fiji','Lithuania','Comoros','Niger','Moldova','Mayotte','Papua N Guinea','Lesotho','India',
              'Guadeloupe','Malaysia','Solomon Isl','Bermuda','Chad','Guyana','St Kitts/Nevis','Dominican Rep',
              'New Caledonia','Antigua/Barb','Tahiti','Eritrea','Hong Kong','Grenada','Singapore','Vanuatu',
              'Andorra','South Sudan','Yemen','Afghanistan','Philippines','Puerto Rico','Belize','São Tomé/Pr',
              'Gibraltar','St Vincent/Gren','Saint Lucia','Barbados','Somaliland','Western Sahara','Dominica',
              'Liechtenstein','Bonaire','Montserrat','Greenland','Aruba','Mauritius','Nepal','Myanmar','Maldives',
              'Monaco','Taiwan','Somalia','Seychelles','Pakistan','Djibouti','Bahamas','Cambodia','Bangladesh',
              'Cayman Islands','Saint Martin','Mongolia','San Marino','Sint Maarten','Chagos Islands','Tuvalu',
              'Turks & Caicos','St Barthélemy','Guam','Wallis and Futuna','Macao','Vatican','Cook Islands',
              'Samoa','St Pierre/Miquel','Sri Lanka','US Virgin Isl','Laos','Tibet','East Timor','Anguilla',
              'Br Virgin Islands','Brunei','Falkland Islands','FS Micronesia','Bhutan','Kiribati','Tonga','Niue',
              'Eastern Samoa','N Marianas','Palau','Swaziland','Libya','Netherlands Antilles']

newData=newData.replace(to_replace=Country_simp,value=Country_full)
# print(newData.head())

#%%
#OutPuut file

newData.to_csv("Elo_cleanData.csv", index = None)
