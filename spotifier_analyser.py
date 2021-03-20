import json
import spotipy
import pandas as pd
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import sys
import gc
import os
from sklearn.preprocessing import MinMaxScaler
from math import pi
import io
import matplotlib.pyplot as plt

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=sys.argv[1],
                                               client_secret=sys.argv[2],
                                               redirect_uri=sys.argv[3],
                                               scope="user-library-read"))
#playlist_id='' #insert your playlist id

for i in range (0,5):
    results = sp.current_user_saved_tracks()

    ids=[]

    for idx, item in enumerate(results['items']):
            track = item['track']['id']
            ids.append(track)
            
    song_meta={'id':[],'album':[], 'name':[], 
            'artist':[],'explicit':[],'popularity':[]}

    for song_id in ids:
        # get song's meta data
        meta = sp.track(song_id)
        
        # song id
        song_meta['id'].append(song_id)

        # album name
        album=meta['album']['id']
        song_meta['album']+=[album]

        # song name
        song=meta['name']
        song_meta['name']+=[song]
        
        # artists name
        s = ', '
        artist=s.join([singer_name['name'] for singer_name in meta['artists']])
        song_meta['artist']+=[artist]
        
        # explicit: lyrics could be considered offensive or unsuitable for children
        explicit=meta['explicit']
        song_meta['explicit'].append(explicit)
        
        # song popularity
        popularity=meta['popularity']
        song_meta['popularity'].append(popularity)

    song_meta_df=pd.DataFrame.from_dict(song_meta)

    # check the song feature
    features = sp.audio_features(song_meta['id'])
    # change dictionary to dataframe
    features_df=pd.DataFrame.from_dict(features)

    # convert milliseconds to mins
    # duration_ms: The duration of the track in milliseconds.
    # 1 minute = 60 seconds = 60 × 1000 milliseconds = 60,000 ms
    features_df['duration_ms']=features_df['duration_ms']/60000

    # combine two dataframe
    final_df=song_meta_df.merge(features_df)
    print('Processing taste '+str(i*25)+'%')
    final_df.to_csv('test.csv', mode='a', header = False, index = False)
    gc.collect()

# column names: id,album,name,artist,explicit,popularity,danceability,energy,key,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo,type,uri,track_href,analysis_url,duration_ms,time_signature
df_dataset = pd.read_csv('test.csv', names = ['id','album','name','artist','explicit','popularity','danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','type','uri','track_href','analysis_url','duration_ms','time_signature'])
df_dataset.to_csv('dataset.csv', index = False)
print('finished!')


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
plt.savefig(os.path.join('templates\\assets','user_stats.png'))

os.remove('test.csv')