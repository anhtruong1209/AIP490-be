from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi import Depends
from services.body_background import BodyBackground
from fastapi.encoders import jsonable_encoder
from models.respone import ResponeModel , HumanbodyRectangle, Body
from models.error import ErrorModel
from models.request import convert_multis_image
import traceback
from PIL import Image
from io import BytesIO
router = APIRouter()
# VITON CLOTHES
@router.post("/viton_clothes")    
def body_background(image: dict = Depends(convert_multis_image)):
    
    image_byte1 = image['image1']
    image_byte2 = image['image2']
    
    if(image_byte1 is None):
        return JSONResponse(content=jsonable_encoder(ErrorModel(error_message="MISSING_ARGUMENTS: image_url1, image_file1, image_base64_1")),
                            status_code=400)
    if(image_byte2 is None):
        return JSONResponse(content=jsonable_encoder(ErrorModel(error_message="MISSING_ARGUMENTS: image_url2, image_file2, image_base64_2")),
                            status_code=400)
    image1 = Image.open(BytesIO(image_byte1))
    image2 = Image.open(BytesIO(image_byte2))
    image_name1 = image["image_name1"]
    image_name2 = image["image_name2"]
    img_path1 = 'data/VITON/VITON_test/test_img/' + image_name1
    image1.save(img_path1)
    img_path2 = 'data/VITON/VITON_test/clothes/' + image_name2
    image2.save(img_path2)
    
    # nparr_image = np.fromstring(image_byte1, np.uint8)
    # human_image = cv2.imdecode(nparr_image, cv2.IMREAD_COLOR)
    
    # nparr_background = np.fromstring(image_byte2, np.uint8)
    # glass_image = cv2.imdecode(nparr_background, cv2.IMREAD_COLOR)

    # return ResponeModel(image=image_byte1)

