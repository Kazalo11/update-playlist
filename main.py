import time
from datetime import date

import schedule
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth


def job():

	print("Checking spotify for latest saved tracks")
	scope = ["user-library-read", "playlist-modify-public", "playlist-modify-private"]
	load_dotenv()

	sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

	latest_tracks = sp.current_user_saved_tracks(50)['items']

	current_playlists = sp.current_user_playlists(10)['items']
	now = date.today()

	formatted_date = now.strftime("%b %y")

	def checkDate(item):
		return item['name'] == formatted_date

	existing_playlist = list(filter(checkDate, current_playlists))
	if existing_playlist != []:
		print("Found playlist for this month")
		playlist_id = existing_playlist[0]['id']

		
	else:
		print("Creating a new playlist")
		info = sp.user_playlist_create("18tta2lvd65imwx89d7mqr2sv",formatted_date)
		playlist_id = info['id']

	playlist = sp.playlist(playlist_id=playlist_id, fields='tracks.items(track(id))')

	playlist_tracks = playlist['tracks']['items']

	track_ids = [item['track']['id'] for item in playlist_tracks]
	print(track_ids)

	latest_tracks.sort(key=lambda x: x["added_at"], reverse=True)

	latest_track_id = latest_tracks[0]['track']['id']
	

	if latest_track_id in track_ids:
		print("Track already found, no need to add again")
		return 
	sp.playlist_add_items(playlist_id, [f'spotify:track:{latest_track_id}'])
	print("Added song to playlist")


schedule.every(1).minutes.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)