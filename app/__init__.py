from config import config 
from flask import Flask, render_template
from app.main import main as main_bp 
from app.auth import auth 
from app.api_1_0 import api 


def create_app ( config_name ):
    app= Flask(__name__)
    app.config.from_object( config[config_name])
    config[config_name].init_app(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth)
    app.register_blueprint(api)
    
    return app 


