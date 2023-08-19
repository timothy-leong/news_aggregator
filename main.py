import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
from os import getenv

scopes = [
    "playlist-modify-public",
    "playlist-modify-private",
    "playlist-read-private",
    "user-read-playback-position",
]

# Set your spotify ID as 'ME' in your environment.
# Also set the spotipy env vars listed here:
# https://spotipy.readthedocs.io/en/2.22.1/#quick-start

# Get my id
user = getenv("ME")

# Set the name of the news aggregation playlist. Note that
# Spotify allows a user to create many playlists with the same name.
playlist_name = "Stay informed"

# Create the client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scopes))

# Create the playlist to add news (only do this once)
# sp.user_playlist_create(user, name=playlist_name, description='An aggregation of news')

# Get the id of the playlist
my_playlists = sp.user_playlists(user)
news_playlist_id = None
while my_playlists["next"]:
    playlists = my_playlists["items"]
    found = False
    for playlist in playlists:
        if playlist["name"] == playlist_name:
            news_playlist_id = playlist["id"]
            found = True
            break
    if found:
        break
    elif my_playlists["next"]:
        playlists = sp.next(my_playlists)
    else:
        print("Cannot find a playlist with the name", playlist_name)
        exit(1)


# Decide which shows you want to catch up on
shows = [
    "7sDXM8BlxsUqzL2IqmLqwE",  # Markets Daily Crypto Roundup
    "05uLjJxkVgQsRk8LWLCLpx",  # Wall Street Breakfast
    "3wBfqov60qDZbEVjPHo0a8",  # BBC Global News Podcast
    "1410RabA4XOqO6IV8p0gYF",  # FT News Briefing
    "2Shpxw7dPoxRJCdfFXTWLE",  # Philosophize This
    "2Mk6QICNrew2ya93Bv3eWX",  # Chat With Traders
    "64cCsH4LCyO5U52xUU4Pax",  # BBC Documentary Podcast
    "4LkuKmIv7MRbpgtTZk3pUX",  # FT World Weekly
]

# Clean out the playlist
items = sp.playlist_items(news_playlist_id, fields="items.track.uri")["items"]
tracks_to_remove = []
for item in items:
    if item["track"] is not None:
        uri = item["track"]["uri"]
        tracks_to_remove.append(uri)
sp.playlist_remove_all_occurrences_of_items(news_playlist_id, tracks_to_remove)

# For each show, take only the latest episode
episodes_to_add = []
for show in shows:
    latest_show = sp.show_episodes(show, limit=1)["items"][0]["uri"]
    episodes_to_add.append(latest_show)
sp.playlist_add_items(news_playlist_id, episodes_to_add)
