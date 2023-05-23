import os
import sys
import copy
import argparse
import warnings
import base64
import numpy as np
import cv2

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from config import settings
from PIL import Image
from services.bodybackground.modnet import MODNet
warnings.filterwarnings("ignore")

class BodyBackground(object):
    def __init__(self):
        # define hyper-parameters
        self.ref_size = 512
        # define image to tensor transform
        self.im_transform = transforms.Compose(
            [
                transforms.ToTensor(),
                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
            ]
        )
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        # create MODNet and load the pre-trained ckpt
        self.modnet = MODNet(backbone_pretrained=False)
        self.modnet = nn.DataParallel(self.modnet)
        self.parameter_load('pretrained/modnet_photographic_portrait_matting.ckpt')
        print("Body background built")
        
    def parameter_load(self, ckpt_path):
        self.modnet.load_state_dict(
            torch.load(ckpt_path, map_location=self.device))
        self.modnet.eval()

    def dir_check(self, path):
        os.makedirs(path, exist_ok=True)
        if not path.endswith('/'):
            path += '/'
        return path

    def pre_process(self, im):
        self.original_im = copy.deepcopy(im)
        # convert image to PyTorch tensor
        im = self.im_transform(im)

        # add mini-batch dim
        im = im[None, :, :, :]

        # resize image for input
        im_b, im_c, im_h, im_w = im.shape
        self.height, self.width = im_h, im_w

        if max(im_h, im_w) < self.ref_size or min(im_h, im_w) > self.ref_size:
            if im_w >= im_h:
                im_rh = self.ref_size
                im_rw = int(im_w / im_h * self.ref_size)
            elif im_w < im_h:
                im_rw = self.ref_size
                im_rh = int(im_h / im_w * self.ref_size)
        else:
            im_rh = im_h
            im_rw = im_w

        im_rw = im_rw - im_rw % 32
        im_rh = im_rh - im_rh % 32
        im = F.interpolate(im, size=(im_rh, im_rw), mode='area')
        return im
    

    def post_process(self, mask_data, background=False, backgound_path=None):
        matte = F.interpolate(mask_data, size=(
            self.height, self.width), mode='area')
        matte = matte.repeat(1, 3, 1, 1)
        matte = matte[0].data.cpu().numpy().transpose(1, 2, 0)
        height, width, _ = matte.shape
        if background:
            back_image = cv2.resize(
                backgound_path, (width, height), cv2.INTER_AREA)
        else:
            backgound_path = np.full(self.original_im.shape, 255.0)

        self.alpha = np.uint8(matte[:, :, 0]*255)

        matte = matte * self.original_im + (1 - matte) * back_image
        return matte

    def image(self, im, background=True,backgound_path=None, save=False):
   
        im = self.pre_process(im)
        _, _, matte = self.modnet(im, inference=False)
        matte = self.post_process(matte, background, backgound_path)
        h, w, _ = matte.shape
        r_h, r_w = 720, int((w / h) * 720)
        image = cv2.resize(self.original_im, (r_w, r_h), cv2.INTER_AREA)
        matte = cv2.resize(matte, (r_w, r_h), cv2.INTER_AREA)

        _, im_arr = cv2.imencode('.jpg', matte)  # im_arr: image in Numpy one-dim array format.
        im_bytes = im_arr.tobytes()
        im_b64 = base64.b64encode(im_bytes)
        return im_b64

    def inference(self, img, bg_path):
        
        im_b64= self.image(img, background=True,backgound_path= bg_path, save=False)
        return im_b64.decode("utf-8")
    
