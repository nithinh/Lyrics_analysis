from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def kmeans_cluster(data, df, n):
    nan_x, nan_y = np.where(np.isnan(data))
    nan_x = list(set(nan_x))  # 224
    nan_x.sort(reverse=True)

    for i in nan_x:
        df.drop(axis=0, index=i, inplace=True)
        data = np.delete(data, i, axis=0)
    df.reset_index(drop=True, inplace=True)

    # print(data.size)  # 5026 * 300

    kmeans = KMeans(n_clusters=n).fit(data)
    # print(kmeans.labels_)
    # print(kmeans.cluster_centers_)

    return data, kmeans


def calculate_purity(kmeans, n):
    purity_cnt = np.zeros((n, n))
    for index, label in enumerate(kmeans.labels_):
        # print("index: {}, genre: {}, label: {}".format(index, df["genre_map"][index], label))
        purity_cnt[label][df["genre_map"][index]] += 1

    result = np.mean(np.max(purity_cnt, axis=1)/np.sum(purity_cnt, axis=1))
    return result


def visualization(data, labels):
    tsne = TSNE(n_components=2)
    decomposition_data = tsne.fit_transform(data)

    x = []
    y = []
    for i in decomposition_data:
        x.append(i[0])
        y.append(i[1])

    fig = plt.figure(figsize=(15, 15))
    ax = plt.axes()
    plt.scatter(x, y, c=labels, marker="x")
    plt.xticks(())
    plt.yticks(())
    plt.savefig('./cluster.png')
    plt.show()


if __name__== "__main__":

    # Load data, len = 5250
    data = np.load('./updated_embeddings.npy')
    df = pd.read_csv('./updated_song_map.csv')
    n_genres = 6

    new_data, kmeans = kmeans_cluster(data, df, n_genres)
    purity = calculate_purity(kmeans, n_genres)
    visualization(new_data, kmeans.labels_)
