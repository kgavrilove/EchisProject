
class MapGenerator():
    def __init__(self):
        self.initial_colors = {
             'красный': (0, 100, 100, 0),
            'красно-оранжевый': (0, 90, 80, 0),
             'оранжевый': (0, 65, 100, 0),
             'желто-оранжевый': (0, 40, 100, 0),
             'желтый': (0, 0, 100, 0),
             'желто-зеленый': (60, 0, 100, 0),
             'зеленый': (100, 0, 90, 0),
             'сине-зеленый': (100, 0, 40, 0),
             'синий': (100, 60, 0, 0),
             'сине-фиолетовый': (100, 90, 0, 0),
             'фиолетовый': (80, 100, 0, 0),
             'красно-фиолетовый': (40, 100, 0, 0)
        }
        self.color_map = {}

    def stretchingByTone(self, modify=False):
        new_map = {}
        for k, v in self.initial_colors.items():
            counter = 5
            new_map.update({k + '_' + str(counter): v})
            coefficient = 15
            # val=v
            # color_value=list(val)
            for i in range(1, counter, 1):
                color_value = list(v)

                if (modify == True):
                    # модификация
                    c = coefficient * i / 100
                    color_value[0] -= color_value[0] * c
                    color_value[1] -= color_value[1] * c
                    color_value[2] -= color_value[2] * c
                # модификация

                color_value[3] = color_value[3] + coefficient * i

                new_map.update({k + '_' + str(counter - i): tuple(color_value)})

            for i in range(counter - 1, 0, -1):
                c = coefficient * i / 100
                val = v
                color_value = list(val)
                # print(c)
                # print(val)
                color_value[0] -= color_value[0] * c
                color_value[1] -= color_value[1] * c
                color_value[2] -= color_value[2] * c
                color_value[3] = 0.0

                new_map.update({k + '_' + str(counter + i): tuple(color_value)})

            print(k)
            self.color_map = new_map
        return new_map


    def convertToRGB(self ,color):
        red = 255 * (1 - color[0] / 100) * (1 - color[3] / 100)
        green = 255 * (1 - color[1] / 100) * (1 - color[3] / 100)
        blue = 255 * (1 - color[2] / 100) * (1 - color[3] / 100)
        return (red, green, blue)

    def rgb2lab(self ,inputColor):

        num = 0
        RGB = [0, 0, 0]

        for value in inputColor:
            value = float(value) / 255

            if value > 0.04045:
                value = ((value + 0.055) / 1.055) ** 2.4
            else:
                value = value / 12.92

            RGB[num] = value * 100
            num = num + 1

        XYZ = [0, 0, 0, ]

        X = RGB[0] * 0.4124 + RGB[1] * 0.3576 + RGB[2] * 0.1805
        Y = RGB[0] * 0.2126 + RGB[1] * 0.7152 + RGB[2] * 0.0722
        Z = RGB[0] * 0.0193 + RGB[1] * 0.1192 + RGB[2] * 0.9505
        XYZ[0] = round(X, 4)
        XYZ[1] = round(Y, 4)
        XYZ[2] = round(Z, 4)

        XYZ[0] = float(XYZ[0]) / 95.047  # ref_X =  95.047   Observer= 2°, Illuminant= D65
        XYZ[1] = float(XYZ[1]) / 100.0  # ref_Y = 100.000
        XYZ[2] = float(XYZ[2]) / 108.883  # ref_Z = 108.883

        num = 0
        for value in XYZ:

            if value > 0.008856:
                value = value ** (0.3333333333333333)
            else:
                value = (7.787 * value) + (16 / 116)

            XYZ[num] = value
            num = num + 1

        Lab = [0, 0, 0]

        L = (116 * XYZ[1]) - 16
        a = 500 * (XYZ[0] - XYZ[1])
        b = 200 * (XYZ[1] - XYZ[2])

        Lab[0] = round(L, 0)
        Lab[1] = round(a, 0)
        Lab[2] = round(b, 0)

        return Lab

    def generate_color_map(self):
        cmyk_map =self.stretchingByTone()
        map ={}
        for k, v in cmyk_map.items():
            rgb = self.convertToRGB(v)
            lab = self.rgb2lab(rgb)
            map[k] = (lab[0], lab[1], lab[2])
        return map
