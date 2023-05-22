from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from uuid import uuid4
from io import BytesIO
from PIL import Image
from models.error import ErrorModel
import traceback
from fastapi.encoders import jsonable_encoder

def error_media_type():
    return HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                         detail= 'File has unsupported extension type')

def save_one_image(image1):
    image_id = uuid4()
    image1 = Image.open(BytesIO(image1))
    try:
        img_path = f'assets/{str(image_id)[0:8]}.jpg'
        image1.save(img_path)
    except:
        img_path = f'assets/{str(image_id)[0:8]}.png'
        image1.save(img_path)

def error_detect_face():
    return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                         detail= 'Can not detect Face')

def error_exeption():
    error = str(traceback.format_exc())
    return JSONResponse(content=jsonable_encoder(ErrorModel(error_message=error)),
                                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



