import swagger_client
import csv
import json
from collections import Counter
from swagger_client.rest import ApiException
# str | Account api key, to be used in every api call
swagger_client.configuration.api_key['apikey'] = '87ae3b136bd09c9e07f71e2632b8739a'


# create an instance of the API class
api_instance = swagger_client.TrackApi()
format = 'json' # str | output format: json, jsonp, xml. (optional) (default to json)
# callback = 'callback_example' # str | jsonp callback (optional)
# q_artist = 'Lewis Capaldi' # str | The song artist (optional)
# q_track = 'Someone you loved' # str | The song title (optional)
# # f_has_lyrics = 3.4 # float | When set, filter only contents with lyrics (optional)
# # f_has_subtitle = 3.4 # float | When set, filter only contents with subtitles (optional)

# try: 
# 	# 
# 	api_response = api_instance.matcher_track_get_get(format=format,q_artist=q_artist, q_track=q_track)
# 	print(api_response)
# except ApiException as e:
# 	print("Exception when calling TrackApi->matcher_track_get_get: %s\n")


'''
{'message': {'body': {'track': {'album_coverart_100x100': None,
								'album_coverart_350x350': None,
								'album_coverart_500x500': None,
								'album_coverart_800x800': None,
								'album_id': 32470363.0,
								'album_name': 'Divinely Uninspired To A '
											  'Hellish Extent',
								'artist_id': 33258132.0,
								'artist_mbid': None,
								'artist_name': 'Lewis Capaldi',
								'commontrack_id': 89461086.0,
								'commontrack_vanity_id': None,
								'explicit': 0.0,
								'first_release_date': None,
								'has_lyrics': 1.0,
								'has_subtitles': 1.0,
								'instrumental': 0.0,
								'lyrics_id': None,
								'num_favourite': 4984.0,
								'primary_genres': {'music_genre_list': [{'music_genre': {'music_genre_id': 20.0,
																						 'music_genre_name': 'Alternative',
																						 'music_genre_name_extended': 'Alternative',
																						 'music_genre_parent_id': 34.0,
																						 'music_genre_vanity': 'Alternative'}},
																		{'music_genre': {'music_genre_id': 14.0,
																						 'music_genre_name': 'Pop',
																						 'music_genre_name_extended': 'Pop',
																						 'music_genre_parent_id': 34.0,
																						 'music_genre_vanity': 'Pop'}},
																		{'music_genre': {'music_genre_id': 34.0,
																						 'music_genre_name': 'Music',
																						 'music_genre_name_extended': 'Music',
																						 'music_genre_parent_id': 0.0,
																						 'music_genre_vanity': 'Music'}}]},
								'restricted': 0.0,
								'secondary_genres': None,
								'subtitle_id': None,
								'track_edit_url': 'https://www.musixmatch.com/lyrics/Lewis-Capaldi/Someone-You-Loved/edit?utm_source=application&utm_campaign=api&utm_medium=',
								'track_id': 170306150.0,
								'track_isrc': None,
								'track_length': None,
								'track_mbid': None,
								'track_name': 'Someone You Loved',
								'track_name_translation_list': [],
								'track_rating': 99.0,
								'track_share_url': 'https://www.musixmatch.com/lyrics/Lewis-Capaldi/Someone-You-Loved?utm_source=application&utm_campaign=api&utm_medium=',
								'track_soundcloud_id': None,
								'track_spotify_id': None,
								'track_xboxmusic_id': None,
								'updated_time': '2019-07-10T15:49:51Z'}},
			 'header': {'execute_time': 0.073276996612549,
						'status_code': 200.0}}}
'''
def get_genre(response):
	def get_most_likely_genre(genre_list):
		min_genre_id = 5000
		min_genre_name = ''
		for item in genre_list:
			if 'music_genre' in item:
				if 'music_genre_id' in item['music_genre']:
					gen_id = item['music_genre']['music_genre_id']
					if gen_id == 34:
						continue
					if gen_id < min_genre_id:
						min_genre_id = gen_id
						min_genre_name = item['music_genre']['music_genre_name']
		return min_genre_name



	if 'message' in response:
		message = response['message']
		if 'header' in message and 'status_code' in message['header']:
			if message['header']['status_code'] == 200:
				if 'body' in message and 'track' in message['body']:
					track = message['body']['track']
					if 'primary_genres' in track and 'music_genre_list' in track['primary_genres']:
						genres = track['primary_genres']['music_genre_list']
						return get_most_likely_genre(genres)
	return None


genres = []
downloaded_songs = []
i=0
j = 0
with open('songs.json') as json_file:
	data = json.load(json_file)
	for p in data:
		# print(p)
		song_detail = {}
		if 'title' in p and 'artist' in p:
			# print('Name: ' + p['title'])
			# print('Artist: ' + p['artist'])
			song_detail['title'] = p['title']
			song_detail['artist'] = p['artist']
			if 'genre' in p:
				# print('Genre: ' + p['genre'])
				genres.append(p['genre'])
				song_detail['genre'] = p['genre']
			else:
				q_artist = p['artist'] # str | The song artist (optional)
				q_track = p['title'] # str | The song title (optional)
				try: 
	# 
					api_response = api_instance.matcher_track_get_get(format=format,q_artist=q_artist, q_track=q_track)
					# print(api_response)
					genre = get_genre(api_response.to_dict())
					if genre:
						j +=1
						print("Got genre from musix match ",j)
						genres.append(genre)
						song_detail['genre'] = genre

				except ApiException as e:
					print("Exception when calling TrackApi->matcher_track_get_get: %s\n")
			downloaded_songs.append(song_detail)
			
			if (i%20 == 0):
				with open("songs_genres.json","w") as outfile:
					print(len(downloaded_songs), " downloaded from ", i)
					json.dump(downloaded_songs,outfile)
					print("Saved to json file")
				
			i+=1
			
			
with open("songs_genres.json","w") as outfile:
	print(len(downloaded_songs), " downloaded from ", i)
	json.dump(downloaded_songs,outfile)

	print(downloaded_songs)
	print(Counter(genres))
		

