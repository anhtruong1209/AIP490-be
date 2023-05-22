import traceback
from pymongo import MongoClient
from config import settings

class MongoDBConfig(object):
    def __init__(self):
        self.mongo_host = settings.MONGO_HOST
        self.mongo_port = int(settings.MONGO_PORT)
        self.mongo_username = settings.MONGO_USERNAME
        self.db = settings.DB
        self.mongo_pass = settings.MONGO_PASS
        
    def mongo_connect_faceai(self):
        client = MongoClient(f'mongodb://{self.mongo_username}:{self.mongo_pass}@{self.mongo_host}/{self.db}', port=self.mongo_port)
        db = client[self.db]
        print(db)
        return db
    
    def mongodb_init(self):
        try:
            print("mongodb started successfully")
        except:
            print(traceback.format_exc())
            pass

    def logger_init(self):
        db = self.mongo_connect_faceai()
        log_db = db.logger
        return log_db
            
    def mongodb_logger_insert(self, data):
        try:
            log_db = self.logger_init()
            
            log_db.insert_one(data)
            return "logging insert done"
        except:
            print(traceback.format_exc())
            pass

    def mongodb_logger_update(self, filter, update_data):
        try:
            log_db = self.logger_init()
            newvalue = {"$set": update_data}
            log_db.update_one(filter, newvalue)
            return "logging update done"
        except:
            print(traceback.format_exc())
            pass

    def mongodb_logger_findone_bonus(self, data):
        try:
            log_db = self.logger_init()
            find_one_data = log_db.find_one(data)
            # print(x)
            return find_one_data         
        except:
            print(traceback.format_exc())
            pass
            
    def mongodb_logger_find(self, condition):
        try:
            log_db = self.logger_init()
            find_data = log_db.find(condition)
            # print(x)
            return find_data         
        except:
            print(traceback.format_exc())
            pass

m = MongoDBConfig()
#  create example:
db_data = {
            "id_task": "Hello",
            "content": "PENDING",
            "start_time": "",
            "end_time": "",
            "duration": "",
            "item": "",
            "error": "",
            "status": "",
            "venv": ""
        }

a = m.mongodb_logger_insert(db_data)
print(a)