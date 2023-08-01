import glob
import json
from os import path as osp
import random
import numpy as np
from PIL import Image, ImageDraw
import torch
from torch.utils import data
from torchvision import transforms
from torch.nn import functional as F
import pandas as pd
import h5py
import numpy as np

class VITONDataset(data.Dataset):
    def __init__(self, img_names=[], c_names=[]):
        self.mode = 'test'
        super(VITONDataset, self).__init__()
        self.load_height = 256
        self.load_width = 192
        self.data_path = 'services/clothesviton/data/VITON/VITON_test'
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

        self.img_names = img_names
        self.c_names = dict()
        self.c_names['paired'] = c_names
        self.c_names['unpaired'] = c_names
        print(c_names)
        print(img_names)
    def __getitem__(self, index):
        img_name = self.img_names[index]
        c_name = {}
        c = {}
        cm = {}
        for key in self.c_names:
            if key == "unpaired":
                continue
            else:
                c_name[key] = self.c_names[key][index].replace("_0.jpg","_1.jpg")
            c[key] = Image.open(osp.join(self.data_path, 'clothes', c_name[key])).convert('RGB')
            c[key] = transforms.Resize(self.load_width, interpolation=2)(c[key])
            c[key] = self.transform(c[key])  

        pose_name = img_name.replace('.jpg', '_keypoints.jpg')
        pose_rgb = Image.open(osp.join(self.data_path, 'vis_pose', pose_name))
        pose_rgb = transforms.Resize(self.load_width, interpolation=2)(pose_rgb)
        pose_rgb = self.transform(pose_rgb)  

        # load person image
        img = Image.open(osp.join(self.data_path, self.mode+'_img', img_name))
        img = transforms.Resize(self.load_width, interpolation=2)(img)
        img_agnostic = Image.open(osp.join(self.data_path, 'img_agnostic', img_name))
        img_agnostic = transforms.Resize(self.load_width, interpolation=2)(img_agnostic)
        try:
           img = self.transform(img)
        except:
           print(img_name)
           #raise erro
        img_agnostic = self.transform(img_agnostic)  # [-1,1]
        if self.mode =='train' and random.random()>0.5:
            c['paired'] = torch.flip(c['paired'],[2])
            result = {
            'img_name': img_name,
            'c_name': c_name,
            'img': torch.flip(img,[2]),
            'img_agnostic': torch.flip(img_agnostic,[2]),
           'pose': torch.flip(pose_rgb,[2]),
           'cloth': c,
            }
        else:
            result = {
            'img_name': img_name,
            'c_name': c_name,
            'img': img,
            'img_agnostic': img_agnostic,
            'pose': pose_rgb,
            'cloth': c,
            }
        return result
    def __len__(self):
        return len(self.img_names)
