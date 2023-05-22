from typing import List, Optional
from pydantic import BaseModel
from uuid import uuid4, UUID

class HumanbodyRectangle(BaseModel):
    top: Optional[int]  
    left: Optional[int] 
    width: Optional[int] 
    height: Optional[int] 
    
class Body(BaseModel):
    area: Optional[HumanbodyRectangle] = None
    pose: dict = None
    
class ResponeModel(BaseModel):
    request_id: UUID = uuid4()
    image: Optional[str] = None
    bodies: List[Body] = []
    image_id: UUID = uuid4()

class ResponeAnalyzeModel(BaseModel):
    request_id: UUID = uuid4()
    analyze: dict
    image_id: UUID

class FaceRectangle(BaseModel):
    top: Optional[int]  
    left: Optional[int] 
    width: Optional[int] 
    height: Optional[int] 

class FaceDetection(BaseModel):
    score: float = None
    area: FaceRectangle = None
    landmarks: dict = None
    attributes: dict = None
    
class Attributes(BaseModel):
    emotion: dict = None
    dominant_emotion: str
    # race: dict = None
    # dominant_race: str
    age: int
    gender: str
        
class FaceDetectionListRepone(BaseModel):
    request_id: UUID = uuid4()
    faces: List[FaceDetection]
    image_id:  UUID = uuid4()

class ImageSame(BaseModel):
    url: str
    distance: float

class FaceSearchRepone(BaseModel):
    request_id: UUID = uuid4()
    similar_faces: List[ImageSame] = []
    different_faces: List[ImageSame] =[]
    face:FaceDetection
    image_id:  UUID = uuid4()

class ResponeVerifyModel(BaseModel):
    request_id: UUID = uuid4()
    verified: bool
    distance: float
    threshold: float
    face1: FaceDetection = None
    face2: FaceDetection = None
    image_id1: UUID
    image_id2: UUID
    
def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }
