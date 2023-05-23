# configs.py

"""===========Library=========="""
from code import interact
from lib2to3.pgen2.token import OP
from pathlib import Path
from typing import Optional, List, cast
from pydantic import BaseSettings, Field, BaseModel
import logging

class LoggingConfig(BaseSettings):
    LOGGING_LEVEL: int = logging.INFO

class DirectoryBaseConfig(BaseModel):
    """Base Configurations."""
    # all the directory level information defined at app config level
    # we do not want to pollute the env level config with these information
    # this can change on the basis of usage
    BASE_DIR: Path = Path(__file__).resolve().parent

    # models directory
    MODELS_DIR: Path = BASE_DIR.joinpath('pretrained')
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

class FileType(BaseModel):
    """Body Outlining"""
    # Net settings
    FILE: Optional[str] = 'file'
    URL: Optional[str] = 'url'
    BASE64: Optional[str] = 'base64'
"""Services Image """
class AnimeModels(BaseModel):
    PHOTO2CARTOON_WEIGHTS: Optional[str] = 'pretrained/photo2cartoon_weights.pt'
    MODEL_MOBILEFACE_NET: Optional[str] = 'pretrained/model_mobilefacenet.pth'
    SEG_MODEL_384: Optional[str] = 'pretrained/seg_model_384.pb'

"""Services Body"""
# class BodyDetectionModels(BaseModel):
#     YOLO_V3_CFG: Optional[str] = 'pretrained/yolov3.cfg'
#     YOLO_V3_TXT: Optional[str] = 'pretrained/yolov3.txt'
#     YOLO_V3_WEIGHTS: Optional[str] = 'pretrained/yolov3.weights'
class BodySkeletonModels(BaseModel):
    CHECK_POINT: Optional[str] = 'pretrained/checkpoint.pth'

    
"""----------GLOBAL CONFIGUATIONS----------"""
class GlobalConfig(BaseSettings):
    # Create APP_CONFIG objects
    DIRECTORY_BASE_CONFIG: DirectoryBaseConfig = DirectoryBaseConfig()
    # BODY_DETECTION_MODEL: BodyDetectionModels = BodyDetectionModels()
    # BODY_SKELETON_MODEL: BodySkeletonModels = BodySkeletonModels()
    # ANIME_MODEL: AnimeModels = AnimeModels()
    FILE_TYPE : FileType = FileType()
    # API settings
    API_NAME: Optional[str] =  None
    API_DESCRIPTION: Optional[str] =  None
    API_ENDPOINT: Optional[str] = None
    API_VERSION: Optional[str] = None
    API_DEBUG_MODE: Optional[bool] = None

    # CORSMiddleware Settings
    CORSMIDDLEWARE_MAX_AGE: Optional[int] = Field(None, env="CORSMIDDLEWARE_MAX_AGE")
    CORSMIDDLEWARE_ALLOW_CREDENTIALS: Optional[bool] = Field(None, env="CORSMIDDLEWARE_ALLOW_CREDENTIALS")
    CORSMIDDLEWARE_ALLOW_METHODS: Optional[list] = Field(None, env="CORSMIDDLEWARE_ALLOW_METHODS")
    CORSMIDDLEWARE_ALLOW_HEADERS: Optional[list] = Field(None, env="CORSMIDDLEWARE_ALLOW_HEADERS")
    CORSMIDDLEWARE_ALLOW_ORIGINS: Optional[list] = Field(None, env="CORSMIDDLEWARE_ALLOW_ORIGINS")

    # Define global variableƒbas with the Field class
    ENV_STATE: Optional[str] = Field(None, env="ENV_STATE")

    # Logging configuration file
    LOG_CONFIG_FILENAME: Optional[str] = Field(None, env="LOG_CONFIG_FILENAME")

    # Environment specific variables do not need the Field class  https://www.uvicorn.org/
    HOST: Optional[str] = None
    # Port
    PORT: Optional[int] = None
    # Name Queue 
    QUEUE_NAME: Optional[str] = None
    HOST_QUEUE: Optional[str] =  Field(None, env="HOST_QUEUE")
    PORT_QUEUE: Optional[str] = Field(None, env="PORT_QUEUE")
    
    # [critical|error|warning|info|debug|trace]
    LOG_LEVEL: Optional[str] =  Field(None, env="LOG_LEVEL")
    USE_COLORS: Optional[bool] =  Field(None, env="USE_COLORS")
    WORKERS: Optional[str] = Field(None, env="WORKERS")
    RELOAD: Optional[str] = Field(None, env= "RELOAD")
    BASE_URL: Optional[str] = "http://13.215.89.207:8000/"
    # Database setting
    DB: Optional[str] = Field(None, env="DB")
    MONGO_HOST: Optional[str] = None
    MONGO_PORT: Optional[int] = Field(None, env="MONGO_PORT")
    MONGO_USERNAME: Optional[str] = Field(None, env="MONGO_USERNAME")
    MONGO_PASS: Optional[str] = Field(None, env="MONGO_PASS")
    DEVICE = "cpu"
    class Config:
        """Loads the dotenv file."""
        env_file: str = ".env"
        case_sensitive: bool = True


class DevAIConfig(GlobalConfig):
    """Development configurations."""

    class Config:
        env_prefix: str = "DEVAI_"
        
class DevAPPConfig(GlobalConfig):
    """Local configurations."""
    
    class Config:
        env_prefix: str = "DEVAPP_"

class StagingConfig(GlobalConfig):
    """Statging configurations."""
    
    class Config:
        env_prefix: str = "STAGING_"

class ProdConfig(GlobalConfig):
    """Production confijugurations."""

    class Config:
        env_prefix: str = "PROD_"

class FactoryConfig:
    """Returns a config instance depending on the ENV_STATE variable."""

    def __init__(self, env_state: Optional[str]):
        self.env_state = env_state

    def __call__(self):
        if self.env_state == "devai":
            return DevAIConfig()

        elif self.env_state == "prod":
            return ProdConfig()
        
        elif self.env_state == "devapp":
            return DevAPPConfig()
        
        elif self.env_state == "staging":
            return StagingConfig()


settings = FactoryConfig(GlobalConfig().ENV_STATE)()

