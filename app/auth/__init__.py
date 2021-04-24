from flask import Blueprint

auth = Blueprint("auth", __name__, prefix="/auth/") 

from . import views, errors 
