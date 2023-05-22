from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi import Depends
import cv2, traceback
import numpy as np
from services.deepface import DeepFace
from services.retinaface.retinaface import RetinaFace
from fastapi.encoders import jsonable_encoder
from models.respone import ResponeModel
from models.error import ErrorModel
from models.request import convert_single_image, convert_multis_image
from models.respone import (FaceDetectionListRepone, FaceDetection, FaceRectangle, Attributes, 
                            FaceSearchRepone, ImageSame, ResponeVerifyModel)
from uuid import uuid4
from PIL import Image
from io import BytesIO
from config import settings
router = APIRouter()

image_path = "assets/db/8.jpg"

DeepFace.analyze(img_path = image_path)
RetinaFace.detect_faces(image_path)
DeepFace.find(img_path= image_path, db_path= 'assets/my_db',model_name='ArcFace', detector_backend= 'ssd')
DeepFace.verify(img1_path = image_path,img2_path = image_path)

@router.post("/face_analyze")
async def face_analyze(image: dict = Depends(convert_single_image)):
    try:
        if(image is None):
            return JSONResponse(content=jsonable_encoder(ErrorModel(error_message="MISSING_ARGUMENTS:\
                                                        image_url, image_file, image_base64")), status_code=400)
        image_id = uuid4()
        image1 = Image.open(BytesIO(image))
        try:
            img1_path = f'assets/{str(image_id)[0:8]}.jpg'
            image1.save(img1_path)
        except:
            img1_path = f'assets/{str(image_id)[0:8]}.png'
            image1.save(img1_path)

        result = DeepFace.analyze(img_path = img1_path)
        faces = FaceDetection(area=FaceRectangle(left=result["rectangle"]["left"],
                                                 top=result["rectangle"]["top"],
                                                 width=result["rectangle"]["width"],
                                                 height=result["rectangle"]["height"]),
                              attributes=Attributes(emotion=result["emotions"]["details"],
                                                    age=result["age"],
                                                    dominant_emotion=result["emotions"]["status"],
                                                    gender=result["gender"]))
        # Update db error to here 
        
        return FaceDetectionListRepone(faces=[faces],image_id=image_id)
    except Exception:
        # Update db error to here 
        print(traceback.format_exc())
        return JSONResponse(content=jsonable_encoder(ErrorModel(error_message=str(traceback.format_exc()))),
                                    status_code=500)
        
@router.post("/face_detect")
async def face_detect(image: dict = Depends(convert_single_image)):
    try:
        if(image is None):
            return JSONResponse(content=jsonable_encoder(ErrorModel(error_message="MISSING_ARGUMENTS:\
                                                        image_url, image_file, image_base64")), status_code=400)
        image_id = uuid4()
        image1 = Image.open(BytesIO(image))
   
        try:
            img_path = f'assets/{str(image_id)[0:8]}.jpg'
            image1.save(img_path)
        except:
            img_path = f'assets/{str(image_id)[0:8]}.png'
            image1.save(img_path)

       
        resp = RetinaFace.detect_faces(img_path)
        faces = []
        for key,value in resp.items():
            face_rectangle = FaceRectangle(left=value["facial_area"][0],top=value["facial_area"][1],
                                            width=value["facial_area"][2]-value["facial_area"][0],
                                            height=value["facial_area"][3]-value["facial_area"][1])
            landmarks = {}
            for i,j in value["landmarks"].items():
                   landmarks[i] = [j[0].item(),j[1].item()]
            faces.append(FaceDetection(area=face_rectangle,score=value["score"].item(),landmarks=landmarks))
        # print(faces)
        return FaceDetectionListRepone(faces=faces)
    except Exception:
        print(traceback.format_exc())
        return JSONResponse(content=jsonable_encoder(ErrorModel(error_message=str(traceback.format_exc()))),
                                    status_code=500)
       
@router.post("/face_search")
async def face_search(image: dict = Depends(convert_single_image)):
    try:
        if(image is None):
            return JSONResponse(content=jsonable_encoder(ErrorModel(error_message="MISSING_ARGUMENTS:\
                                                         image_url, image_file, image_base64")),status_code=400)
        image_id = uuid4()
        image1 = Image.open(BytesIO(image))
        try:
            img_path = f'assets/{str(image_id)[0:8]}.jpg'
            image1.save(img_path)
        except:
            img_path = f'assets/{str(image_id)[0:8]}.png'
            image1.save(img_path)
        
        model_list = ['VGG-Face', 'Facenet', 'OpenFace', 'DeepFace', 'DeepID', 'Dlib', 'ArcFace', 'Ensemble']
        backends = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface', 'mediapipe']
        result = DeepFace.find(img_path= img_path, db_path= 'assets/db',model_name=model_list[6], detector_backend= backends[1])
        face_rectangle = FaceRectangle(left=result[2][0],top=result[2][1],width=result[2][2],height=result[2][3])
        list_same = []
        list_difference = []
        for key, value in result[0]["identity"].items():
              url = settings.BASE_URL+ value
              distance = result[0]["ArcFace_cosine"][key]
              list_same.append(ImageSame(url=url,distance=distance))
        for key, value in result[1]["identity"].items():
              url = settings.BASE_URL+value
              distance = result[1]["ArcFace_cosine"][key]
              list_difference.append(ImageSame(url=url,distance=distance))   
        return FaceSearchRepone(face=FaceDetection(area=face_rectangle), similar_faces=list_same,different_faces=list_difference)
    except Exception():
        print(traceback.format_exc())
        return JSONResponse(content=jsonable_encoder(ErrorModel(error_message=str(traceback.format_exc()))),
                            status_code=500)

@router.post("/face_verify")
async def face_verify(image: dict = Depends(convert_multis_image)):
    try:
        image_read1 = image["image1"]
        if(image_read1 is None):
            return JSONResponse(content=jsonable_encoder(ErrorModel(error_message="MISSING_ARGUMENTS: image_url1, image_file1, image_base64_1")),
                                status_code=400)
        image_read2 = image["image2"]
        if(image_read2 is None):
            return JSONResponse(content=jsonable_encoder(ErrorModel(error_message="MISSING_ARGUMENTS: image_url2, image_file2, image_base64_2")),
                                status_code=400)
        image1 = Image.open(BytesIO(image_read1))
        image2 = Image.open(BytesIO(image_read2))
        image_id1 = uuid4()
        image_id2 = uuid4()
        try:
            img1_path = f'assets/{str(image_id1)[0:8]}.jpg'
            image1.save(img1_path)
        except:
            img1_path = f'assets/{str(image_id1)[0:8]}.png'
            image1.save(img1_path)
        try:
            img2_path = f'assets/{str(image_id2)[0:8]}.jpg'
            image2.save(img2_path)
        except:
            img2_path = f'assets/{str(image_id2)[0:8]}.png'
            image2.save(img2_path)

        model_list = ['VGG-Face', 'Facenet', 'OpenFace', 'DeepFace', 'DeepID', 'Dlib', 'ArcFace', 'Ensemble']
        result = DeepFace.verify(img1_path = img1_path,img2_path =  img2_path, model_name = 'ArcFace',
                                distance_metric = 'cosine', model = None, enforce_detection = False,
                                detector_backend = 'ssd', align = None, prog_bar = False, normalization = 'base')
        face_rectangle1=FaceRectangle(left=result['RegionImage1'][0],top=result['RegionImage1'][1],width=result['RegionImage1'][2],height=result['RegionImage1'][3])
        face_rectangle2=FaceRectangle(left=result['RegionImage2'][0],top=result['RegionImage2'][1],width=result['RegionImage2'][2],height=result['RegionImage2'][3])
        return ResponeVerifyModel(image_id1=image_id1,image_id2=image_id2,verified=result['Verified'],
                                  distance=result['Distance'],threshold=result['Threshold'],face1=FaceDetection(area=face_rectangle1),
                                  face2=FaceDetection(area=face_rectangle2))
    except Exception as e:
        print(traceback.format_exc())
        return JSONResponse(content=jsonable_encoder(ErrorModel(error_message=str(traceback.format_exc()))),
                                    status_code=500)

