#pip install billboard.py

import billboard
import time
import pandas as pd
import pickle

def save_dict(songs_dict):
	f = open("songs_dict.pkl", 'wb')
	pickle.dump(songs_dict, f)
	f.close()

def get_billboard_100(iterations, year=1979, month='07', day=20, dict_file='songs_dict.pkl'):
	songs = dict()
	if dict_file:
		with open('songs_dict.pkl', 'rb') as handle:
			songs = pickle.load(handle)


	temp_year = year
	temp_month = month
	temp_date = str(temp_year) + '-' + temp_month + '-' + str(day)

	chart = billboard.ChartData('hot-100')
	for i in range(iterations):
		print(i)
		print(temp_date)
		print(len(songs))

		for song in chart:
			if song not in songs:
				songs[song.title] = (song.artist, song.weeks, song.peakPos)

		save_dict(songs)
		time.sleep(4)

		if temp_month == '11':
			temp_month = '07'
		elif temp_month == '07':
			temp_month = '03'
		elif temp_month == '03':
			temp_month = '11'
			temp_year -= 1

		temp_date = str(temp_year) + '-' + temp_month + '-' + str(day)
		chart = billboard.ChartData('hot-100', temp_date)

		'''
		if i % 10 == 0:
			songs_to_csv(songs, temp_date)
			print("saved")
		'''

	#print(chart.previousDate)
	return songs

def songs_to_csv(songs_dict):
	songs = songs_dict.keys()
	songs1 = [song for song in songs]
	artists = [songs_dict[song][0] for song in songs]
	weeks = [songs_dict[song][1] for song in songs]
	poss = [songs_dict[song][2] for song in songs]

	songs_df = pd.DataFrame({'songs' : songs1, 'artists' : artists, 'weeks' : weeks, 'peak position' : poss})
	songs_df.to_csv("songs_list.csv", index=False)

def main():
	iterations = 0
	songs = get_billboard_100(iterations)
	songs_to_csv(songs)

if __name__ == '__main__':
	main()