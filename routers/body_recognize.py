from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi import Depends
# from services.body_detection import BodyDetection
# from services.body_skeleton import BodySkeleton
from services.body_background import BodyBackground
from fastapi.encoders import jsonable_encoder
from models.respone import ResponeModel , HumanbodyRectangle, Body
from models.error import ErrorModel
from models.request import convert_single_image, convert_multis_image
from common.read_image import Utils
import traceback, cv2, base64
import numpy as np
from fastapi import File, UploadFile, Form
router = APIRouter()
# bd = BodyDetection()
# bk = BodySkeleton()
bb = BodyBackground()

# @router.post("/body_detect")
# async def body_detection(image_read: dict = Depends(convert_single_image)):
#     try:
#         """Accept fast running task."""
#         if(image_read is None):
#             return JSONResponse(content=jsonable_encoder(ErrorModel(error_message="MISSING_ARGUMENTS:\
#                                                                     image_url, image_file, image_base64")),
#                                 status_code=400) 
#         locations, size = bd.inference(image_read)
#         humanbodies = []
#         for i in locations:
#             humanbodies.append(Body(area=HumanbodyRectangle(left=i[0],top=i[1],
#                                                             width=i[2],height=i[3])))
#         # Update db error to here 
#         return ResponeModel(bodies=humanbodies)
#     except Exception:
#         # Update db error to here 
#         print(traceback.format_exc())
#         return JSONResponse(content=jsonable_encoder(ErrorModel(error_message=str(traceback.format_exc()))),
#                                     status_code=500)

@router.post("/body_background", response_model=ResponeModel, status_code=200)    
def body_background(my_file1: UploadFile = File(...), my_file2: UploadFile = File(...)):
    try:
        image_byte1 = my_file1
        if(image_byte1 is None):
            return JSONResponse(content=jsonable_encoder(ErrorModel(error_message="MISSING_ARGUMENTS: image_url1, image_file1, image_base64_1")),
                                status_code=400)
        image_byte2 = my_file2
        if(image_byte2 is None):
            return JSONResponse(content=jsonable_encoder(ErrorModel(error_message="MISSING_ARGUMENTS: image_url2, image_file2, image_base64_2")),
                                status_code=400)
        nparr_image = np.fromstring(image_byte1, np.uint8)
        img = cv2.imdecode(nparr_image, cv2.IMREAD_COLOR)
        
        nparr_background = np.fromstring(image_byte2, np.uint8)
        bg = cv2.imdecode(nparr_background, cv2.IMREAD_COLOR)
        return_matte = bb.inference(img,bg)

        return ResponeModel(image=return_matte)
    except Exception:
        print(traceback.format_exc())
        return JSONResponse(content=jsonable_encoder(ErrorModel(error_message=str(traceback.format_exc()))),
                                    status_code=500)


        
# @router.post("/body_skeleton", response_model=ResponeModel, status_code=200) 
# async def body_skeleton(image_read: dict = Depends(convert_single_image)):
#     try:   
#         if(image_read is None):
#             return JSONResponse(content=jsonable_encoder(ErrorModel(error_message="MISSING_ARGUMENTS:\
#                                                         image_url, image_file, image_base64")),
#                                 status_code=400)
#         base64Image, humans = bk.inference(image_read)
#         body = []
#         for i in humans:
#             body.append(Body(pose=i))

#         return ResponeModel(bodies=body,image=base64Image)
#     except Exception:
        
#         print(traceback.format_exc())
#         return JSONResponse(content=jsonable_encoder(ErrorModel(error_message=str(traceback.format_exc()))),
#                                     status_code=500)