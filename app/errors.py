from app.database import db_session 
from app.lib.utils import Rest
from marshmallow import ValidationError 
from jwt.exceptions import DecodeError

LOGGED_OUT_TOKEN = 10 
EXPIRED_TOKEN = 11
INVALID_TOKEN = 12 
NO_TOKEN_PROVIDED = 13 
RESOURCE_NOT_FOUND = 14 
VALIDATION_FAILED = 15

class ColorAppException(Exception):
    def __init__(self, code, message, status_code):
        super().__init__(code, message, status_code)
        self.code = code 
        self.message = message 
        self.status_code = status_code


def register_error_handlers(app):
    
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove() 


    @app.errorhandler(ColorAppException)
    def color_app_exception( err : ColorAppException):
        return Rest.error(
            code=err.code , 
            message=err.message,
            response_code=400
        )

    @app.errorhandler(404)
    def resource_not_found(err):
        return Rest.error(
            response_code=404, 
            message="requested resource not found",
            code=RESOURCE_NOT_FOUND)


    @app.errorhandler(400)
    def resource_not_found(err):
        return Rest.error(
            response_code=404, 
            message="requested resource not found",
            code=RESOURCE_NOT_FOUND)


    @app.errorhandler(DecodeError)
    def decode_error(e):
        return Rest.error(
            response_code=400, 
            message="Invalid token", 
            code=INVALID_TOKEN
        )
        
    @app.errorhandler(ValidationError)
    def validation_error( err: ValidationError):
        message = err.messages 
        if isinstance(message, list) : message = message[0]
        
        return Rest.error(
            code=VALIDATION_FAILED, 
            message=message
        )