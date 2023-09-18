from dotenv import load_dotenv
import os
import base64
from requests import post
from requests import get
import json
import pandas as pd
from csv import writer
import random

df = pd.DataFrame()

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

#acquires token to use Spotify API
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers={
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data={
        "grant_type": "client_credentials"
    }

    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("NO ONE EXISTS")
        return None

    return json_result[0]

#extracts songs from an artist
def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    #country = any 2 digit country code

    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    if len(json_result) == 0:
        print("NO ONE EXISTS")
        return None
    return json_result

#extracts albums from an artist
def get_artist_albums(token, artist_id):
    url=f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]

    return json_result

#extracts the songs on a specific album
def get_songs_on_album(token, album_id):
    url =f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["items"]
    return json_result

#acquires the popularity level of a song (based on Spotify data)
def get_popularity_of_song(token, song_id):
    url =f"https://api.spotify.com/v1/tracks/{song_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

#extracts features/attributes of a specific song
def get_song_features(token, song_id):
    url = f"https://api.spotify.com/v1/audio-features/{song_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

singer = input("Please give an artist: ")
artist_list = [singer]

for singer in artist_list:
    token = get_token()
    result = search_for_artist(token, singer)
    artist_id = result["id"]
    songs = get_songs_by_artist(token, artist_id)
    albums = get_artist_albums(token, artist_id)

    print("\n")

    #lists top songs of an artist
    print("Top Songs:")
    for idx, song in enumerate(songs):
        print(f"{idx + 1}. {song['name']}")

    full_discography = []

    print("\n")
    print("Albums:")
    for index, album in enumerate(albums):
        if album['total_tracks'] > 5:
            album_list = []
            print(f"{index + 1}. {album['name']}")
            tracklist = get_songs_on_album(token, album['id'])
            #print("\nSongs on Album:")
            for num, track in enumerate(tracklist):
                popularity = get_popularity_of_song(token, track['id'])
                song_features = get_song_features(token, track['id'])


                df = df.append({'Artist' : popularity['artists'][0]['name'], 'Song' : track['name'], 'Popularity' : popularity['popularity'],
                'Danceability' : song_features['danceability'], 'Energy': song_features['energy'], 'Instrumentalness' : song_features['instrumentalness'],
                'Loudness': song_features['loudness'], 'Speechiness': song_features['speechiness'], 'Valence': song_features['valence'] },ignore_index = True)


                album_list.append((popularity['artists'][0]['name'], track['name'], popularity['popularity']))

            median = df['Popularity'].quantile(q=0.4)
            full_discography.append([album_list, median])
            df.drop(df.index, inplace=True)
        else:
            index-=1

#list to hold underrated tracks of artist
underrated_tracks = []

#adds songs from artist that have lesser popularity (bottom 40% of songs in terms of popularity) onto list
for num in range(len(full_discography)):
    alb_median = full_discography[num][1]
    for x in range(len(full_discography[num][0])):
        if full_discography[num][0][x][2] < alb_median:
            underrated_tracks.append(full_discography[num][0][x][1])

underrated_tracks = list(dict.fromkeys(underrated_tracks))
print('\n')
print(f"Lesser Known Picks from {singer}: \n")
num_list = []
#randomly selects 8 lesser known songs from artists (after collecting list of lesser-known songs)
for n in range(8):
    n = random.randint(0, len(underrated_tracks)-1)
    while n in num_list:
        n = random.randint(0, len(underrated_tracks)-1)

    num_list.append(n)
    print(underrated_tracks[n])
