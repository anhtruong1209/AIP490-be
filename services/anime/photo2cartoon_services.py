import torch, base64, cv2
import numpy as np
from services.anime.photo2cartoon import ResnetGenerator
from utility.anime_utility.photo2cartoon.utils import Preprocess
from config import settings

class Photo2Cartoon:
    def __init__(self):
        self.pre = Preprocess()
        self.device = torch.device(settings.DEVICE)
        self.net = ResnetGenerator(ngf=32, img_size=256, light=True).to(self.device)
        
        params = torch.load(settings.ANIME_MODEL.PHOTO2CARTOON_WEIGHTS, map_location=self.device)
        self.net.load_state_dict(params['genA2B'])
        print('[Step1: load weights] success!')

    def inference(self, img):
        # face alignment and segmentation
        face_rgba, rectangle = self.pre.process(img)
        if face_rgba is None:
            print('[Step2: face detect] can not detect face!!!')
            return None
        
        print('[Step2: face detect] success!')
        face_rgba = cv2.resize(face_rgba, (256, 256), interpolation=cv2.INTER_AREA)
        face = face_rgba[:, :, :3].copy()
        mask = face_rgba[:, :, 3][:, :, np.newaxis].copy() / 255.
        face = (face*mask + (1-mask)*255) / 127.5 - 1

        face = np.transpose(face[np.newaxis, :, :, :], (0, 3, 1, 2)).astype(np.float32)
        face = torch.from_numpy(face).to(self.device)

        # inference
        with torch.no_grad():
            cartoon = self.net(face)[0][0]

        # post-process
        cartoon = np.transpose(cartoon.cpu().numpy(), (1, 2, 0))
        cartoon = (cartoon + 1) * 127.5
        cartoon = (cartoon * mask + 255 * (1 - mask)).astype(np.uint8)
        cartoon = cv2.cvtColor(cartoon, cv2.COLOR_RGB2BGR)
        print('[Step3: photo to cartoon] success!')
        return cartoon, rectangle

        
    def processed_image(self, img):
        try:
            nparr = np.fromstring(img, np.uint8)
            im_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            im_rgb = im_bgr[:, :, [2, 1, 0]]
            cartoon, rectangle = self.inference(im_rgb)
            # print(type(cartoon))
            _, im_arr = cv2.imencode('.jpg', cartoon)  # im_arr: image in Numpy one-dim array format.
            im_b64 = base64.b64encode(im_arr.tobytes()) # to base64
            return im_b64.decode("utf-8"), rectangle
        except:
            return None, None