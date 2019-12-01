import spotipy
import csv
import spotipy.util as util

# username
scope = 'user-library-read'
# export SPOTIPY_CLIENT_ID '64ff1e46f79e4056b783e418605e5f1f'
# export SPOTIPY_CLIENT_SECRET '3f687b7b7bcc462084a58f3dba62346b'
# token = util.prompt_for_user_token(username,scope,client_id='64ff1e46f79e4056b783e418605e5f1f',client_secret='3f687b7b7bcc462084a58f3dba62346b')
sp = spotipy.Spotify()


i = 0
downloaded_songs = []
with open("songs_list.csv") as csvfile:
	reader = csv.DictReader(csvfile, delimiter=',')
	for row in reader:
		song = row['songs']
		artist = row['artists']
		print(song)
		results = sp.search(q='artist:' + artist, type='artist')
		print(results)

