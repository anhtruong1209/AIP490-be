from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from models.request import convert_single_image
from models.error import ErrorModel
from fastapi.encoders import jsonable_encoder
import PIL
import traceback
from PIL import ImageDraw
import easyocr
from fastapi import Depends
# router = APIRouter()
# im = PIL.Image.open("assets/jp2.jpg")
# reader = easyocr.Reader(['ja'])
# bounds = reader.readtext("assets/jp2.jpg")
@router.post("/ocr")
async def ocr(image_read: dict = Depends(convert_single_image)):
    try:
        # """Accept fast running task."""
        # if(image_read is None):
        #     return JSONResponse(content=jsonable_encoder(ErrorModel(error_message="MISSING_ARGUMENTS:\
        #                                                             image_url, image_file, image_base64")),
        #                         status_code=400) 
        # # show an image
        
        # im = PIL.Image.open(image_read)
        # reader = easyocr.Reader(['ja'])
        # bounds = reader.readtext(image_read)
        # # Draw bounding boxes
        # def draw_boxes(image, bounds, color='yellow', width=2):
        #     draw = ImageDraw.Draw(image)
        #     text_all = []
        #     for bound in bounds:
        #         p0, p1, p2, p3 = bound[0]
        #         text_all.append(bound[1])
        #         draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
        #     return image, text_all

        # a, b = draw_boxes(im, bounds)
        # print(b)
        return "OK"
    except Exception:
        print(traceback.format_exc())
        return JSONResponse(content=jsonable_encoder(ErrorModel(error_message=str(traceback.format_exc()))),
                                    status_code=500)