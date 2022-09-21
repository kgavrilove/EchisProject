import cv2

import numpy as np
from sklearn.cluster import KMeans


class ColorExtractor:
    def __init__(self, n_clusters=5):
        self.kmeans = KMeans(n_clusters)

    def get_colors(self, img):
        if img is None:
            raise Exception("image cant be empty")

        s = self.kmeans.fit(img)
        labels = self.kmeans.labels_
        centroid = self.kmeans.cluster_centers_

        labels = list(labels)
        percent = []
        for i in range(len(centroid)):
            j = labels.count(i)
            j = j / (len(labels))
            percent.append(j)

        rounded_centroids = np.round(centroid).astype(int)

        return rounded_centroids, percent
