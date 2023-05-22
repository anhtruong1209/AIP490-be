from io import BytesIO
import numpy as np
import cv2
from PIL import Image
from config import settings

class BodyDetection(object):
    def __init__(self):
        self.labels_path = settings.BODY_DETECTION_MODEL.YOLO_V3_TXT
        weights_path = settings.BODY_DETECTION_MODEL.YOLO_V3_WEIGHTS
        self.config_path = settings.BODY_DETECTION_MODEL.YOLO_V3_CFG
        self.net = cv2.dnn.readNetFromDarknet(self.config_path,weights_path)
        print("Body detection built")
        
    def inference(self, image):
        image = Image.open(BytesIO(image))
        image = np.array(image)
        img_size = Image.fromarray(image)
        size = img_size.size
        H, W, _ = image.shape
        LABELS = open(self.labels_path).read().strip().split("\n")
    
        ln = self.net.getLayerNames()
        ln = [ln[i - 1] for i in self.net.getUnconnectedOutLayers()]

        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),swapRB=True, crop=False)

        self.net.setInput(blob)
        
        layerOutputs = self.net.forward(ln)
        boxes = []
        confidences = []
        classID = []
        result = []

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]
                if(LABELS[classID]=='person' and confidence > 0.7):
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
        
        indx = cv2.dnn.NMSBoxes(boxes, confidences, 0.5,0.3)
        if(len(indx)>0):
            for i in indx.flatten():
                result.append(boxes[i])
        return result, size