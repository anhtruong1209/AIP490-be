import base64
import requests
from enum import Enum
import re

class FileType(Enum):
    FILE = "file"
    BASE64 = 'base64'
    URL = 'url'

class FormatImage(object):
    def __init__(self, image_url, image_file, image_base64):
        self.image_url = image_url
        self.image_file = image_file
        self.image_base64 = image_base64
    
    def isFileFormatCorrect(self):
        return self.image_url or self.image_file or self.image_base64
    @staticmethod
    def url_to_bytes(img):
        return base64.b64decode(img)
    @staticmethod
    def convert_to_byte(img,type):
        try:
            if(type == FileType.FILE):
                return img.file.read()
                
            if(type == FileType.BASE64):
                x = re.sub(r'^data:image\/\w+;base64,', '', img)
                return base64.b64decode(x)
            if(type == FileType.URL):
                response = requests.get(img)
                return response.content
        except Exception as e:
            raise Exception(str(e)) 


    def get_byte_file(self):
        if(self.image_file):
            return self.convert_to_byte(self.image_file,FileType.FILE)
        if(self.image_base64 and self.image_base64!="null"):
            return self.convert_to_byte(self.image_base64,FileType.BASE64)
        if(self.image_url):
            return self.convert_to_byte(self.image_url,FileType.URL)
        return None
        
    
