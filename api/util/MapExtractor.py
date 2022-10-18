import copy
import random

from collections import Counter

import numpy
import numpy as np
from PIL import Image, ImageCms
from matplotlib import colors
from scipy.spatial import cKDTree as KDTree
from scipy.misc import face

from api.util.ClosetTree import ClosetTree


class MapExtractor:
    def __init__(self):
        self.tree = ClosetTree()
        self.MAP_COLORS_HEX = {
            'red': '#E3001B',
            'red-orange': '#E03835',
            'orange': '#EA7305',
            'orange-yellow': '#F4A803',
            'yellow': '#FFEE05',
            'yellow-green': '#7CB51A',
            'green': '#01914C',
            'green-blue': '#0199A4',
            'blue': '#015DA8',
            'blue-purple': '#02368A',
            'purple': '#582483',
            'purple-red': '#A8017A',
            'white': '#ffffff',
            'black': '#000000',
        }
        self.MAP_COLORS_LAB = {
            'red': (56, 83, 66),
            'red-orange': (59, 77, 57),
            'orange': (68, 56, 80),
            'orange-yellow': (78, 33, 88),
            'yellow': (93, -4, 100),
            'yellow-green': (66, -50, 69),
            'green': (50, -76, 26),
            'green-blue': (54, -54, -20),
            'blue': (36, -6, -54),
            'blue-purple': (23, 16, -59),
            'purple': (28, 45, -45),
            'purple-red': (43, 70, -12),
            'white': (100, -0, 0),
            'black': (0, 0, 0),
        }

    def beautufyCounts(self, counts):
        temp = {}

        colors = {k: v for k, v in counts.items() if k not in ['white', 'black']}

        total_pixels = sum(colors.values())
        for key, value in colors.items():
            if value > total_pixels / 500:
                temp[str(key)] = round(value / total_pixels, 4)

        return temp

    def getMapRGB(self, img, beautify='true'):

        REDUCED_COLOR_SPACE = False

        # borrow a list of named colors from map
        if REDUCED_COLOR_SPACE:
            use_colors = {k: colors.cnames[k] for k in
                          ['yellow', 'red', 'blue', 'green', 'purple', 'orange', 'black', 'white']}
        else:
            use_colors = self.MAP_COLORS_HEX

        # translate hexstring to RGB tuple
        named_colors = {k: tuple(map(int, (v[1:3], v[3:5], v[5:7]), 3 * (16,)))
                        for k, v in use_colors.items()}

        counts = self.tree.get_closet(img, named_colors)

        if beautify == 'true':
            output = self.beautufyCounts(counts)
        else:
            output = counts

        return self.beautufyCounts(counts)

    def getMapLAB(self, img, beautify='true'):

        counts = self.tree.get_closet(img, self.MAP_COLORS_LAB)

        if beautify == 'true':
            output = self.beautufyCounts(counts)
        else:
            output = counts

        return output
