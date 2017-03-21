from __future__ import print_function    # (at top of module)
from unidecode import unidecode
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotipy
import time
import sys

text_file = open('missing_2010Singles.txt','w')
song_dup = 0;
## Spotify API Setup
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

## READ CSV
fixed_df = pd.read_csv('WikiSingles2010.csv')
for index, row in fixed_df.iterrows():
    print("Index: %d "%index)
    value = fixed_df.iloc[index]['Song Name']
    song = value.split('(',1)
    song[0] = song[0].rstrip()
    print("\'"+song[0]+"\'")

    song_count = 0;
    ## Search
    result = sp.search(song)
    song_found  = False;
    for i, t in enumerate(result['tracks']['items']):
        # text_file.write("{} by" .format(t['name']).lower())
        # text_file.write(" {}\n" .format(t['artists'][0]['name']).lower())
        try:
            sBool = unidecode(t['name']).lower()==song[0].lower()
        except UnicodeEncodeError:
            text_file.write("UnicodeEncodeError")
        except UnicodeDecodeError:
            text_file.write("UnicodeDecodeError")

        if(sBool):
            urn = t['album']['uri']
            album = sp.album(urn)
            if('2010' in album['release_date']):
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
            with open('singles_output2010.csv', 'a') as f:
                try:
                    df.to_csv(f, header=False)
                except UnicodeEncodeError:
                    text_file.write("UnicodeEncodeError")
            break
            # song_count +=1
            # print(song_count)

    if not(song_found):
        for i, t in enumerate(result['tracks']['items']):
            try:
                text_file.write("{}\n" .format(unidecode(t['name'])).lower())
            except UnicodeEncodeError:
                text_file.write("UnicodeEncodeError")

        text_file.write("Missing Song @ index: {} " .format(index))
        text_file.write("{} \n" .format(song[0]))


text_file.close()
