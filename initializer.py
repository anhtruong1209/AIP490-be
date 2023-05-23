
class IncludeAPIRouter(object):
    def __new__(cls):
        # from routers.face_recognize import router as router_face_recognize
        from routers.body_recognize import router as router_body_recognize
        # from routers.ocr_japanese import router as router_ocr_japanese
        # from routers.image_recognize import router as router_image_recognize
        from fastapi.routing import APIRouter
        router = APIRouter()
        # router.include_router(router_face_recognize, prefix='/v1', tags=['face_recognize'])
        router.include_router(router_body_recognize, prefix='/v1', tags=['body_recognize'])
        # router.include_router(router_image_recognize, prefix='/v1', tags=['image_recognize'])
        # router.include_router(router_ocr_japanese, prefix='/v1', tags=['ocr_japanese'])
        return router
