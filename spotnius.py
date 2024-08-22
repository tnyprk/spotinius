import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup
import webbrowser
import time

# Spotify API credentials
SPOTIPY_CLIENT_ID = 'd4fcd8931bc749b2899411e25c9f6281'
SPOTIPY_CLIENT_SECRET = '0113d1d9a41c484abccd6fb6bad6c93f'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'
SCOPE = 'user-read-currently-playing'

# Genius API credentials
GENIUS_ACCESS_TOKEN = '2Q67X-fVEBpTUoLbZWFtz50s-B2xPlujxL1hhbvTmVvdaCNTdWXgrPN03C_eca-l'

# Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=SCOPE))

def get_current_track():
    current_track = sp.current_user_playing_track()
    if current_track is not None:
        return current_track['item']['name'], current_track['item']['artists'][0]['name']
    return None, None

def search_song_on_genius(song_name, artist_name):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': f'Bearer {GENIUS_ACCESS_TOKEN}'}
    search_url = f'{base_url}/search'
    params = {'q': f'{song_name} {artist_name}'}
    
    response = requests.get(search_url, headers=headers, params=params)
    return response.json()

def get_lyrics_url(song_data):
    for hit in song_data['response']['hits']:
        if hit['type'] == 'song':
            return hit['result']['url']
    return None

def main():
    previous_track = None
    
    while True:
        song_name, artist_name = get_current_track()
        
        if song_name and artist_name and (song_name, artist_name) != previous_track:
            print(f"Now playing: {song_name} by {artist_name}")
            
            song_data = search_song_on_genius(song_name, artist_name)
            lyrics_url = get_lyrics_url(song_data)
            
            if lyrics_url:
                print(f"Lyrics found: {lyrics_url}")
                webbrowser.open(lyrics_url)
            else:
                print("Lyrics not found.")
            
            previous_track = (song_name, artist_name)
        
        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    main()
