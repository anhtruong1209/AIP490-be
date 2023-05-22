from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi import Depends, status
from utility.validation.error import (error_media_type, save_one_image,
                                     error_detect_face, error_exeption)
import traceback
from fastapi.encoders import jsonable_encoder
from models.respone import ResponeModel, FaceDetection, FaceRectangle
from models.request import convert_single_image
from services.anime.photo2cartoon_services import Photo2Cartoon
import numpy as np
import cv2
p2c = Photo2Cartoon()
router = APIRouter()
@router.post('/anime_photo2cartoon')
async def face_analyze(image: dict = Depends(convert_single_image)):
    """End point for uploading a file"""
    try:
        if(image is None): 
            error_media_type()
        save_one_image(image)

        return_img, box = p2c.processed_image(image)
        if return_img != None:
            face_rectangle = []
            face_rectangle.append(FaceDetection(
                                 area=FaceRectangle(left=box[0],top=box[2]-box[0],
                                 width=box[0],height=box[2]-box[0])))
            return ResponeModel(image=return_img, face= face_rectangle)
        else:
            error_detect_face()
    except Exception:
        error_exeption()



