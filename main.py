from datetime import date

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth


def main():


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
		playlist_id = existing_playlist[0]['id']

		
	else:
		info = sp.user_playlist_create("18tta2lvd65imwx89d7mqr2sv",formatted_date)
		playlist_id = info['id']

	playlist = sp.playlist(playlist_id=playlist_id, fields='tracks.items(track(id))')

	latest_tracks.sort(key=lambda x: x["added_at"])

	latest_track_id = latest_tracks[-1]['track']['id']

	if latest_track_id in playlist:
		return 
	sp.playlist_add_items(playlist_id, [f'spotify:track:{latest_track_id}'])


main()