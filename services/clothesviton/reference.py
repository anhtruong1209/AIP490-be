import os
import torch.backends.cudnn as cudnn
import torch
from torch import nn
from torch.nn import functional as F
import tqdm
import numpy as np
from PIL import Image
from services.clothesviton.datasets import VITONDataset
from services.clothesviton.models.sdafnet import SDAFNet_Tryon
from torch.utils import data
from torchvision.utils import save_image
import base64

cudnn.benchmark = True

def test(net, img_name, c_name):
    
    img_base64 = ''
    test_dataset = VITONDataset(img_name, c_name)
    test_loader = data.DataLoader(test_dataset, batch_size=4, shuffle=True,num_workers=4)
    for i, inputs in enumerate(tqdm.tqdm(test_loader)):
        img_names = inputs['img_name']
        cloth_names = inputs['c_name']['paired']
        img = inputs['img']
        img_agnostic = inputs['img_agnostic'] #Masked model image
        pose = inputs['pose']
        cloth_img = inputs['cloth']['paired']
        img =  F.interpolate(img, size=(256, 192), mode='bilinear')
        cloth_img = F.interpolate(cloth_img, size=(256, 192), mode='bilinear')
        img_agnostic = F.interpolate(img_agnostic, size=(256, 192), mode='bilinear')
        pose = F.interpolate(pose, size=(256, 192), mode='bilinear')
        ref_input = torch.cat((pose, img_agnostic), dim=1)
        tryon_result = net(ref_input, cloth_img, img_agnostic).detach()
        for j in range(tryon_result.shape[0]):
            save_image(tryon_result[j:j+1], os.path.join('./results/', 'TEST_UNPAIR', "vis_viton_out", img_names[j]), nrow=1, normalize=True, range=(-1,1))
            with open(f'services/clothesviton/results/TEST_UNPAIR/vis_viton_out/{img_names[j]}', "rb") as img_file:
                my_string = base64.b64encode(img_file.read())
    img_base64 = my_string.decode("utf-8")
    return img_base64 

def reference(img_name, c_name):
    name = 'TEST_UNPAIR'
    save_dir = 'services/clothesviton/results/'
    if not os.path.exists(os.path.join(save_dir, name, "vis_viton_out")):
        os.makedirs(os.path.join(save_dir, name,"vis_viton_out"))
    sdafnet = SDAFNet_Tryon(ref_in_channel=6)
    sdafnet.load_state_dict(torch.load("services/clothesviton/pretrained/ckpt_viton.pt", map_location='cpu'))
    sdafnet.eval()    
    a =  test(sdafnet, img_name, c_name)
    return a
