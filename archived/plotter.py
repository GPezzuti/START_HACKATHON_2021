from sklearn.preprocessing import MinMaxScaler
from math import pi
import pandas as pd
import io
import os

#BPM range is 0 to 200 bpm, converting to percentage
df_dataset = pd.read_csv('dataset.csv')
df_dataset['tempo'] = df_dataset['tempo']/2.05

df_dataset['duration_ms'] = df_dataset['duration_ms']/0.04

#Loudness is from -60db to 0 db
df_dataset['loudness'] = df_dataset['loudness']*(-1)
df_dataset['loudness'] = 25-df_dataset['loudness']
df_dataset['loudness'] = df_dataset['loudness']/0.25

print(df_dataset.head())

music_feature = df_dataset[['danceability','energy','loudness','speechiness','acousticness','instrumentalness','liveness','valence','tempo','duration_ms']]
min_max_scaler = MinMaxScaler()
music_feature.loc[:]=min_max_scaler.fit_transform(music_feature.loc[:])

import matplotlib.pyplot as plt

# plot size
fig=plt.figure(figsize=(12,8))

# convert column names into a list
categories=list(music_feature.columns)
# number of categories
N=len(categories)

# create a list with the average of all features
value=list(music_feature.mean())

# repeat first value to close the circle
# the plot is a circle, so we need to "complete the loop"
# and append the start value to the end.
value+=value[:1]
# calculate angle for each category
angles=[n/float(N)*2*pi for n in range(N)]
angles+=angles[:1]

# plot
plt.polar(angles, value)
plt.fill(angles,value,alpha=0.3)

# plt.title('Discovery Weekly Songs Audio Features', size=35)

plt.xticks(angles[:-1],categories, size=15)
plt.yticks(color='grey',size=15)
plt.savefig(os.path.join('templates','user_stats.png'))