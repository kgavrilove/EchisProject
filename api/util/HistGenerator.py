import cv2

class HistGenerator:
    def __init__(self):
        pass

# rgb image
    def get_histograms(self,image):
        if image is None:
            raise Exception("image cant be empty")

        red_histogram = cv2.calcHist([image], [0], None, [256], [0, 256])
        blue_histogram = cv2.calcHist([image], [1], None, [256], [0, 256])
        green_histogram = cv2.calcHist([image], [2], None, [256], [0, 256])

        return red_histogram, blue_histogram, green_histogram

