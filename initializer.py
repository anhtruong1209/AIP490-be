
class IncludeAPIRouter(object):
    def __new__(cls):
        from routers.body_recognize import router as router_body_recognize
        from fastapi.routing import APIRouter
        router = APIRouter()
        router.include_router(router_body_recognize, prefix='/v1', tags=['body_recognize'])
        return router
