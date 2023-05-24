import cv2
import numpy as np
import base64
class GlassFace(object):
    def __init__(self):
        # Load model
        self.face_detection_model = cv2.CascadeClassifier("pretrained/haarcascade_frontalface_alt.xml")
        self.eye_detection_model = cv2.CascadeClassifier("pretrained/haarcascade_eye.xml")
        
        print("GlassFace Model Load Done")
    def process_image(self, human_image, glass_image):
        final_image = human_image
        # 1. Phát hiện khuôn mặt
        gray_image = cv2.cvtColor(human_image, cv2.COLOR_BGR2GRAY)

        faces = self.face_detection_model.detectMultiScale(gray_image, scaleFactor=1.3, minNeighbors=5, minSize=(200,200))
        
        if len(faces) > 0:
            for (face_x, face_y, face_w, face_h) in faces:

                # 2. Phát hiện mắt
                eye_centers = []
                face_roi = gray_image[face_y: face_y + face_h, face_x : face_x + face_w]

                eyes = self.eye_detection_model.detectMultiScale(face_roi, scaleFactor=1.1, minNeighbors=5, minSize=(100,100))

                # Lấy tâm của 2 mắt
                for (eye_x, eye_y, eye_w, eye_h) in eyes:
                    eye_centers.append((face_x + int(eye_x + eye_w/2), face_y + int(eye_y + eye_h/2)))

                if len(eye_centers) >=2:

                    # 3. Tính toán toạ độ và kích thước của kính
                    glass_width_resize = 2.5 * abs(eye_centers[1][0] - eye_centers[0][0])
                    scale_factor = glass_width_resize / glass_image.shape[1]

                    resize_glasses = cv2.resize(glass_image, None, fx= scale_factor, fy=scale_factor)

                    # Tính toạ đọ của kính
                    if eye_centers[0][0] <  eye_centers[1][0]:
                        left_eye_x = eye_centers[0][0]
                    else:
                        left_eye_x = eye_centers[1][0]

                    glass_x = left_eye_x - 0.28 * resize_glasses.shape[1]
                    glass_y = face_y + 0.8 * resize_glasses.shape[0]

                    # 4. Vẽ kính lên mặt

                    overlay_image = np.ones(human_image.shape, np.uint8)  * 255
                    overlay_image [int(glass_y): int(glass_y + resize_glasses.shape[0]),
                                    int(glass_x): int(glass_x + resize_glasses.shape[1])] = resize_glasses


                    gray_overlay = cv2.cvtColor(overlay_image, cv2.COLOR_BGR2GRAY)
                    _, mask = cv2.threshold(gray_overlay, 127, 255, cv2.THRESH_BINARY)

                    # Lấy phần background và face (trừ phần kính mắt) ra khỏi ảnh gốc
                    background = cv2.bitwise_and(human_image, human_image, mask = mask)

                    mask_inv = cv2.bitwise_not(mask)

                    # Lấy phần kính ra khỏi overlay
                    glasses = cv2.bitwise_and(overlay_image, overlay_image, mask=mask_inv)

                    final_image = cv2.add(background, glasses)
        
        _, im_arr = cv2.imencode('.jpg', final_image)
        im_bytes = im_arr.tobytes()
        im_b64 = base64.b64encode(im_bytes)
        return im_b64

