import datetime

import cv2
import imutils
from api.util.ColorExtractor import ColorExtractor
from api.util.HistGenerator import HistGenerator


class AssetService():
    def __init__(self):
        self.hist_generator = HistGenerator()

    def resize(self, img, scale_percent=60):
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)

        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

        return resized

    def generate_info(self, img_name,k_clusters=5):
        img=imutils.url_to_image(img_name)

        img = self.resize(img)

        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.reshape((image.shape[1] * image.shape[0], 3))

        color_extractor = ColorExtractor(k_clusters)

        rounded_centroids, percent = color_extractor.get_colors(img)
        red_histogram, blue_histogram, green_histogram = self.hist_generator.get_histograms(image)

        image_data = {
            'image': img_name,
            'kMeans': {
                'k_clusters':k_clusters,
                'dominantColors': rounded_centroids,
                'percentage': percent,
            },
            'histogram': {
                'red': red_histogram,
                'blue': blue_histogram,
                'green': green_histogram
            },

        }
        print(rounded_centroids)
        print(percent)
        return image_data
