import numpy as np
from scipy.spatial import KDTree


class ClosetTree:
    def __init__(self):
        self.param = ''

    def get_closet(self, img, named_colors):

        ncol = len(named_colors)

        color_tuples = list(named_colors.values())
        color_tuples = np.array(color_tuples)

        color_names = list(named_colors)

        tree = KDTree(color_tuples[:-1])
        # tolerance for color match `inf` means use best match no matter how
        # bad it may be
        tolerance = np.inf
        # find closest color in tree for each pixel in picture
        dist, idx = tree.query(img, distance_upper_bound=tolerance)
        # count and reattach names
        counts = dict(zip(color_names, np.bincount(idx.ravel(), None, ncol + 1)))

        return counts
