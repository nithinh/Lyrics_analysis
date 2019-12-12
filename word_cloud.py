import numpy as np
import pandas as pd
import re
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def genre_count(groups, n):

    count = np.zeros(n)
    for i, genre in groups:
        count[i] = len(genre)

    plt.style.use('seaborn')

    X = np.arange(n) + 1
    Y = count

    plt.bar(X, Y,
        tick_label=['Pop', 'Hip Hop', 'Folk, World\n& Country', 'Electronic', 'Funk / Soul', 'Rock'],
        color=['#E74C3C', '#AF7AC5', '#5DADE2', '#48C9B0', '#F4D03F', '#EB984E'])

    for x, y in zip(X, Y):
        plt.text(x, y, int(y), ha='center', va='bottom')

    plt.xlabel("Genre")
    plt.ylabel("Number")
    # plt.savefig('graphs/genre_number.png', dpi=200)
    plt.show()


def word_cloud(groups):
    plt.figure()
    for i, genre in groups:
        plt.subplot(2, 3, i+1)
        # print(genre)
        songs = genre["preprocessed_lyrics"].values
        words = []
        for song in songs:
            song = re.sub("\[|\]|\'|\s", "", song)
            words.extend(song.split(","))

        # print(len(words))
        cloud_dict = {}
        for index, (word, count) in enumerate(Counter(words).most_common(45)):
            if index > 15:
                cloud_dict[word] = count
        # print(cloud_dict)
        plt.style.use('seaborn')
        wc = WordCloud(
            scale=2,
            max_font_size=100,
            background_color='#383838',  # 383838
            colormap='Oranges')

        wc.generate_from_frequencies(frequencies=cloud_dict)

        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
    plt.tight_layout()
    plt.savefig('graphs/word_clouds_top15-45.png', dpi=200)
    plt.show()


if __name__== "__main__":

    # load data
    df = pd.read_csv('./updated_song_map.csv')
    groups = df.groupby('genre_map')
    n_genres = 6

    # Count the entries of each genre and plot
    # genre_count(groups, n_genres)

    # Creating word cloud for each genre
    word_cloud(groups)
