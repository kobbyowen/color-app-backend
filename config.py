import os 
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "34ewqdwq4e3wqe13213wq234weqe313ewqededs324"
    TOKEN_LIFETIME_IN_SECONDS = 3 * 24 * 3600 # 3 days 

    @staticmethod
    def init_app(app):
        pass 

class ProductionConfig(Config):
    DEBUG = False 
    DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///myDB.db'

class DevelopmentConfig(Config):
    DEBUG = True 
    DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///myDB.db'

class TestingConfig(Config):
    TESTING= True 
    DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///myDB.db'


config = {
    "development" : DevelopmentConfig ,
    "production" : ProductionConfig, 
    "testing": TestingConfig,
    'default' : DevelopmentConfig
}