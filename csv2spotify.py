from __future__ import print_function    # (at top of module)
from unidecode import unidecode
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotipy
import time
import sys

text_file = open('missing_2013.txt','w')
song_missing = 0;
## Spotify API Setup
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

## READ CSV
fixed_df = pd.read_csv('Billboard_2013.csv')
for index, row in fixed_df.iterrows():
    print("Index: %d "%index)
    song = fixed_df.iloc[index]['Title']
    artist = fixed_df.iloc[index]['Artist']
    # song = value.split('(',1)
    print(song)

    song_count = 0;
    ## Search
    result = sp.search(str(song)+" "+str(artist))
    song_found  = False;
    for i, t in enumerate(result['tracks']['items']):

        # text_file.write("{} by" .format(t['name']).lower())
        # text_file.write(" {}\n" .format(t['artists'][0]['name']).lower())

        if(unidecode(t['name']).lower().find(song.lower())>-1 and unidecode(t['artists'][0]['name']).lower()==artist.lower()):
            song_found = True

            # if(song_count > 1):
            #     song_dup+=1;
            #     text_file.write("Song Number: {} ".format(song_dup))
            #     text_file.write("Info: {}\n".format(t['name']+" by "+t['artists'][0]['name']))
            # else:
                # print(t['name'],t['id'])
            tids = str(t['id'])
            # print(type(tids))
            features = sp.audio_features(tids)
            try:
                features[0]['Song'] = unidecode(t['name'])
            except TypeError:
                break
            features[0]['Artist'] = unidecode(t['artists'][0]['name'])
            json_text = json.dumps(features, indent=4)
            df = pd.read_json(json_text)
            with open('output_2013.csv', 'a') as f:
                try:
                    df.to_csv(f, header = False)
                except UnicodeEncodeError:
                    text_file.write("UnicodeEncodeError")
            break
            # song_count +=1
            # print(song_count)

    if not(song_found):
        song_missing+=1
        for i, t in enumerate(result['tracks']['items']):
            try:
                text_file.write("{} by" .format(unidecode(t['name'])).lower())
            except UnicodeEncodeError:
                    text_file.write("UnicodeEncodeError")
            try:
                text_file.write(" {}\n" .format(unidecode(t['artists'][0]['name'])).lower())
            except UnicodeEncodeError:
                    text_file.write("UnicodeEncodeError")
        text_file.write("Missing Song @ index: {} " .format(index))
        text_file.write("{}\n" .format(song+" by "+artist))


text_file.write("Total number of songs missing: {}\n" .format(song_missing))
text_file.close()
