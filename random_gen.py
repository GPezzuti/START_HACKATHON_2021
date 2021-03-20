import pandas as pd
import numpy as np 
import io 
import os
import gc

df = pd.read_csv('cars_random.csv')
print(df.head())

df['danceability']=np.random.uniform(0.01, 1.0, size=len(df))
df['energy']=np.random.uniform(0.01, 1.0, size=len(df))
df['loudness']=np.random.uniform(-23.001,-0.01, size=len(df))
df['speechiness']=np.random.uniform(0.01, 1.0, size=len(df))
df['acousticness']=np.random.uniform(0.01, 1.0, size=len(df))
df['instrumentalness']=np.random.uniform(0.01, 1.0, size=len(df))
df['liveness']=np.random.uniform(0.01, 1.0, size=len(df))
df['valence']=np.random.uniform(0.01, 1.0, size=len(df))
df['tempo']=np.random.uniform(0.0, 205.0, size=len(df))
df['duration_ms']=np.random.uniform(0.1, 5.0, size=len(df))

print(df.head())
df.to_csv('cars_random_f.csv',header=True, index = False)