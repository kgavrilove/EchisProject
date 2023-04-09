import datetime
import random

import cv2
import imutils
import urllib.request

import numpy as np
from PIL import Image
from PIL import ImageCms
from skimage import color
from skimage.color import rgb2lab

from api.util.ColorExtractor import ColorExtractor
from api.util.HistGenerator import HistGenerator
from api.service.BackgroundService import BackgroundService
from api.util.ImgToMap import ImgToMap
from api.util.MapExtractor import MapExtractor
from api.util.MapCounter import MapCounter


class AssetService():
    def __init__(self):
        self.hist_generator = HistGenerator()
        self.background_service = BackgroundService()
        self.mapper = MapExtractor()
        self.counter = MapCounter()
        self.ImgToMap = ImgToMap()

    def resize(self, img, scale_percent=60):
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)

        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

        return resized

    def rgb_to_lab(self, img):
        srgb_profile = ImageCms.createProfile("sRGB")
        lab_profile = ImageCms.createProfile("LAB")

        rgb2lab_transform = ImageCms.buildTransformFromOpenProfiles(srgb_profile, lab_profile, "RGB", "LAB")
        lab_im = ImageCms.applyTransform(img, rgb2lab_transform)
        return lab_im

    def generate_info(self, img_name, k_clusters=5):
        img = imutils.url_to_image(img_name)

        img = self.resize(img)

        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.reshape((image.shape[1] * image.shape[0], 3))

        color_extractor = ColorExtractor(k_clusters)

        rounded_centroids, percent = color_extractor.get_colors(img)
        red_histogram, blue_histogram, green_histogram = self.hist_generator.get_histograms(image)

        image_data = {
            'image': img_name,
            'kMeans': {
                'k_clusters': k_clusters,
                'dominantColors': rounded_centroids.tolist(),
                'percentage': percent,
            },
            'histogram': {
                'red': red_histogram.tolist(),
                'blue': blue_histogram.tolist(),
                'green': green_histogram.tolist()
            },

        }

        return image_data

    def iten_map(self, img_url, mode='rgb'):

        # exception
        if img_url is None:
            raise Exception("image url cant be empty")

        splited_img = self.background_service.splitimage(img_url)

        urllib.request.urlretrieve(img_url, "asset.png")

        original_img = Image.open("asset.png")

        background = Image.new('RGBA', splited_img['background'].size, (255, 255, 255))
        frontground = Image.new('RGBA', splited_img['frontground'].size, (255, 255, 255))
        back = Image.alpha_composite(background, splited_img['background']).convert("RGB")
        # back.save('C:\\Users\\Kirill\\PycharmProjects\\EchisProject\\static\\' + 'back' + '.png')
        front = Image.alpha_composite(frontground, splited_img['frontground']).convert("RGB")
        # front.save('C:\\Users\\Kirill\\PycharmProjects\\EchisProject\\static\\' + 'front' + '.png')

        if mode == 'lab':
            original_img = self.rgb_to_lab(original_img)
            back = self.rgb_to_lab(back)
            front = self.rgb_to_lab(front)
            original_map = self.mapper.getMapLAB(original_img)
            background_map = self.mapper.getMapLAB(back)
            frontground_map = self.mapper.getMapLAB(front)
            map = self.mapper.MAP_COLORS_LAB
        else:
            original_map = self.mapper.getMapRGB(original_img)
            background_map = self.mapper.getMapRGB(back)
            frontground_map = self.mapper.getMapRGB(front)
            map = self.mapper.MAP_COLORS_HEX

        image_data = {
            'image': img_url,
            'split': {
                'original': original_img,
                'background': splited_img['background'],
                'frontground': splited_img['frontground']
            },
            'mode': mode,
            'map': map,
            'iten_map': {
                'original': original_map,
                'background': background_map,
                'frontground': frontground_map
            },
        }
        return image_data

    def get_map_from_img(self,img , alpha_channel='true'):
        rgb = img.resize((100, 100))

        if alpha_channel == 'true':
            rgb = color.rgba2rgb(rgb)

        lab = color.rgb2lab(rgb)
        image_map = self.ImgToMap.get_map(lab)
        return image_map
    def iten_colors(self, img_url):

        # exception
        if img_url is None:
            raise Exception("image url cant be empty")

        splited_img = self.background_service.splitimage(img_url)

        urllib.request.urlretrieve(img_url, "asset.png")

        original_img = Image.open("asset.png")

        background_map=self.get_map_from_img(splited_img['background'])
        frontground_map = self.get_map_from_img(splited_img['frontground'])
        original_map= self.get_map_from_img(original_img,alpha_channel='false')
        image_data = {
            'image': img_url,
            'split': {
                'original': original_img,
                'background': splited_img['background'],
                'frontground': splited_img['frontground']
            },
            'iten_map': {
                'original': original_map,
                'background': background_map,
                'frontground': frontground_map
            },
        }
        return image_data

    def counts(self, img_url):
        if img_url is None:
            raise Exception("image url cant be empty")

        urllib.request.urlretrieve(img_url, "asset.png")

        original_img = Image.open("asset.png")
        original_img = original_img.resize((100, 100), Image.ANTIALIAS)
        lab_img = color.rgb2lab(np.array(original_img))
        data = self.counter.getCounts(lab_img)
        image_data = {
            'image': img_url,
            'output': data,
        }
        return image_data
