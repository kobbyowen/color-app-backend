from flask import Blueprint

api = Blueprint("api", __name__, prefix="/api/v1.0/") 

from . import views 
from . import errors 
