import numpy as np
import cv2

class Utils:
    def __init__(self, image_1, image_2):
        self.image_1 = image_1
        self.image_2 = image_2
    def read_image(self):
        nparr_image = np.fromstring(self.image_1, np.uint8)
        image_1 = cv2.imdecode(nparr_image, cv2.IMREAD_COLOR)
        
        nparr_background = np.fromstring(self.image_1, np.uint8)
        image_2 = cv2.imdecode(nparr_background, cv2.IMREAD_COLOR)
        return image_1, image_2