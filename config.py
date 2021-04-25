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
    DATABASE_PASSWORD = ""
    DATABASE_USERNAME = ""
    DATABASE_URI = f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@localhost/color-app"

class DevelopmentConfig(Config):
    DEBUG = True 
    DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'data', 'data3.sqlite')}"

class TestingConfig(Config):
    TESTING= True 
    DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'data', 'testing3.sqlite')}"


config = {
    "development" : DevelopmentConfig ,
    "production" : ProductionConfig, 
    "testing": TestingConfig,
    'default' : DevelopmentConfig
}