import pandas as pd
import io 
import os
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
from math import pi
import numpy as np

#Add the car name here
car_name = "cls"

df_dataset = pd.read_csv('dataset.csv')

df_car = pd.read_csv('cars_random_f.csv')
print(df_car.head())
print(df_car.columns)

df_car = df_car.loc[df_car['id'] == str(car_name)]

#Checking highest similarity between user's playlist and car personality.

df_dataset['danceability']=abs(df_dataset['danceability']-df_car.iloc[0,1])
df_dataset['energy']=abs(df_dataset['energy']-df_car.iloc[0,2])
df_dataset['loudness']=abs(df_dataset['loudness']-df_car.iloc[0,3])
df_dataset['speechiness']=abs(df_dataset['speechiness']-df_car.iloc[0,4])
df_dataset['acousticness']=abs(df_dataset['acousticness']-df_car.iloc[0,5])
df_dataset['instrumentalness']=abs(df_dataset['instrumentalness']-df_car.iloc[0,6])
df_dataset['liveness']=abs(df_dataset['liveness']-df_car.iloc[0,7])
df_dataset['valence']=abs(df_dataset['valence']-df_car.iloc[0,8])
df_dataset['tempo']=abs(df_dataset['tempo']-df_car.iloc[0,9])
df_dataset['duration_ms']=abs(df_dataset['duration_ms']-df_car.iloc[0,10])

df_dataset=df_dataset.loc[(df_dataset['danceability']<=0.001) | (df_dataset['energy']<=0.001) | (df_dataset['loudness']<=0.001) | (df_dataset['speechiness']<=0.001) | (df_dataset['acousticness']<=0.001) | (df_dataset['instrumentalness']<=0.001) | (df_dataset['liveness']<=0.001) | (df_dataset['valence']<=0.001) | (df_dataset['tempo']<=0.001) | (df_car['duration_ms']<=0.001)]

#Finding similarity feature between car and human
values = [df_dataset['danceability'].mean(),df_dataset['energy'].mean(), df_dataset['loudness'].mean(), df_dataset['speechiness'].mean(), df_dataset['acousticness'].mean(),
        df_dataset['instrumentalness'].mean(), df_dataset['liveness'].mean(), df_dataset['valence'].mean(), df_dataset['tempo'].mean(), df_dataset['duration_ms'].mean()]

similarity = values.index(min(values))
#similarity = min(df_dataset['danceability'].mean(),df_dataset['energy'].mean(), df_dataset['loudness'].mean(), df_dataset['speechiness'].mean(), df_dataset['acousticness'].mean(),
#        df_dataset['instrumentalness'].mean(), df_dataset['liveness'].mean(), df_dataset['valence'].mean(), df_dataset['tempo'].mean(), df_dataset['duration_ms'].mean())

#The result custom playlist and most similar feature from algo
df_dataset = df_dataset.drop(df_dataset.columns[0], axis=1)

df_dataset.to_csv('playlist.csv', index = False)
print('The thing that is most similar feature for you is: '+str(similarity)) #0-9 (features as mentioned before)