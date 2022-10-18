import datetime

import cv2
import io
import imutils
import copy

from api.util.BackgroundExtractor import BackgroundExtractor


class BackgroundService():
    def __init__(self):
        self.bg_extractor = BackgroundExtractor()

    def convert_to_bytes(self, img):
        byteIO = io.BytesIO()
        img.save(byteIO, format='PNG')
        byteArr = byteIO.getvalue()
        return byteArr

    def splitimage_tobytes(self, img_path):
        frontground, background = self.bg_extractor.removeBg(img_path)

        # need copy cause links
        f = copy.deepcopy(frontground)
        b = copy.deepcopy(background)

        data = {
            'frontground': self.convert_to_bytes(f),
            'background': self.convert_to_bytes(b),
        }
        return data

    def splitimage(self, img_path):
        frontground, background = self.bg_extractor.removeBg(img_path)

        data = {
            'frontground': frontground,
            'background': background,
        }
        return data