import os 
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "34ewqdwq4e3wqe13213wq234weqe313ewqededs324"
    
    @staticmethod
    def init_app(app):
        pass 

class ProductionConfig(Config):
    DEBUG = False 
    DATABASE_PASSWORD = ""
    DATABASE_USERNAME = ""
    DATABASE_URI = f"pymysql+mysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@localhost/color-app"

class DevelopmentConfig(Config):
    DEBUG = True 
    DATABASE_URI = f"sqlite:///{os.path.join(basedir, '/data.sqlite')}"

class TestingConfig(Config):
    TESTING= True 
    DATABASE_URI = f"sqlite:///{os.path.join(basedir, '/testing.sqlite')}"

config = {
    "development" : DevelopmentConfig ,
    "production" : ProductionConfig, 
    "testing": TestingConfig,

    'default' : DevelopmentConfig
}