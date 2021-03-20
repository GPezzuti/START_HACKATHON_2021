import json
import spotipy
import pandas as pd
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import sys
import gc
import os

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="",
                                               client_secret="",
                                               redirect_uri="https://localhost/8080",
                                               scope="user-library-read"))
#playlist_id='' #insert your playlist id

for i in range (0,5):
    results = sp.current_user_saved_tracks(limit=50, offset = int(i*50))

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
        album=meta['album']['name']
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
df_dataset.to_csv('dataset.csv')
print('finished!')
os.remove('test.csv')