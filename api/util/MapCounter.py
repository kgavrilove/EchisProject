import math


class MapCounter:
    def __init__(self):
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
        self.colors=list(self.MAP_COLORS_LAB.values())

    def beautufyCounts(self, counts):

        temp = {}

        total_pixels = sum(counts.values())
        for key, value in counts.items():
            if value > total_pixels / 500:
                temp[str(key)] = (round(value / total_pixels, 4) * 100, value)

        return temp

    def getCounts(self, img, beautify='true'):

        height, width, depth = img.shape
        #print(type(img))
        #print(img.shape)
        #print(img)
        stat = {}
        for h in range(height):
            for w in range(width):
                points = self.colors
                target = img[h][w]
                a = min(points,
                        key=lambda point: math.hypot(target[2] - point[2], target[1] - point[1], target[0] - point[0]))
                color = [k for k, v in self.MAP_COLORS_LAB.items() if v == a][0]
                if color in stat.keys():
                    stat[color] = stat[color] + 1
                else:
                    stat[color] = 1

        counts = stat

        if beautify == 'true':
            output = self.beautufyCounts(counts)
        else:
            output = counts

        return output
