from flask import Flask, render_template
from flask_cors import CORS 
from app.main import main as main_bp 
from app.auth import auth 
from app.api_1_0 import api 
from manage import database_commands, test_commands
from config import config 
from app.errors import register_error_handlers
from app.database import create_all_tables

cors = CORS()

def create_app ( config_name ):
    app= Flask(__name__)
    app.config.from_object( config[config_name])
    config[config_name].init_app(app)

    cors.init_app(app)

    register_error_handlers(app)
    app.register_blueprint(database_commands)
    app.register_blueprint(test_commands)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth, url_prefix="/auth/")
    app.register_blueprint(api, url_prefix="/api/v1/")
    
    create_all_tables()

    return app 


