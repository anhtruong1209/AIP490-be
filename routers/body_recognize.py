from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi import Depends
from services.body_background import BodyBackground
from services.glass_virtual_tryon import GlassFace
from fastapi.encoders import jsonable_encoder
from models.respone import ResponeModel , HumanbodyRectangle, Body
from models.error import ErrorModel
from models.request import convert_single_image, convert_multis_image
import traceback, cv2
import numpy as np

router = APIRouter()
# bb = BodyBackground()
gl = GlassFace()
# Glasses Face
@router.post("/glass_face")    
def body_background(image: dict = Depends(convert_multis_image)):
    # glass_image = cv2.imread("assets/glasses_03.png")
    # human_image = cv2.imread("assets/tl2.png")
    image_byte1 = image['image1']
    image_byte2 = image['image2']
    
    nparr_image = np.fromstring(image_byte1, np.uint8)
    human_image = cv2.imdecode(nparr_image, cv2.IMREAD_COLOR)
    
    nparr_background = np.fromstring(image_byte2, np.uint8)
    glass_image = cv2.imdecode(nparr_background, cv2.IMREAD_COLOR)
    final_image = gl.process_image(human_image, glass_image)
    return ResponeModel(image=final_image)


# @router.post("/body_background")    
# def body_background(image: dict = Depends(convert_multis_image)):
#     image_byte1 = image['image1']
#     image_byte2 = image['image2']
#     nparr_image = np.fromstring(image_byte1, np.uint8)
#     img = cv2.imdecode(nparr_image, cv2.IMREAD_COLOR)
#     nparr_background = np.fromstring(image_byte2, np.uint8)
#     bg = cv2.imdecode(nparr_background, cv2.IMREAD_COLOR)
#     return_matte = bb.inference(img,bg)
#     return ResponeModel(image=return_matte)
    # try:
        
        # if(image_byte1 is None):
        #     return JSONResponse(content=jsonable_encoder(ErrorModel(error_message="MISSING_ARGUMENTS: image_url1, image_file1, image_base64_1")),
        #                         status_code=400)
        # image_byte2 = image['image2']
        # if(image_byte2 is None):
        #     return JSONResponse(content=jsonable_encoder(ErrorModel(error_message="MISSING_ARGUMENTS: image_url2, image_file2, image_base64_2")),
        #                         status_code=400)
        # nparr_image = np.fromstring(image_byte1, np.uint8)
        # img = cv2.imdecode(nparr_image, cv2.IMREAD_COLOR)
        
        # nparr_background = np.fromstring(image_byte2, np.uint8)
        # bg = cv2.imdecode(nparr_background, cv2.IMREAD_COLOR)
        # return_matte = bb.inference(img,bg)

        # return ResponeModel(image=return_matte)
    # except Exception:
    #     print(traceback.format_exc())
    #     return JSONResponse(content=jsonable_encoder(ErrorModel(error_message=str(traceback.format_exc()))),
    #                                 status_code=500)
