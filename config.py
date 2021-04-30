import os 
basedir = os.path.abspath(os.path.dirname(__file__))

def get_db_name():
    name = os.environ.get('DATABASE_URL')
    if name : name = name.replace("://", "ql://", 1) 
    else: name =  'sqlite:///myDB.db'
    return name 

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "34ewqdwq4e3wqe13213wq234weqe313ewqededs324"
    TOKEN_LIFETIME_IN_SECONDS = 3 * 24 * 3600 # 3 days 

    @staticmethod
    def init_app(app):
        pass 

class ProductionConfig(Config):
    DEBUG = False 
    DATABASE_URI = get_db_name()

class DevelopmentConfig(Config):
    DEBUG = True 
    DATABASE_URI = get_db_name()

class TestingConfig(Config):
    TESTING= True 
    DATABASE_URI = get_db_name() 


config = {
    "development" : DevelopmentConfig ,
    "production" : ProductionConfig, 
    "testing": TestingConfig,
    'default' : DevelopmentConfig
}