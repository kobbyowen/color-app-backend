from flask import Blueprint, request 
from app.lib.decorators import load_user_from_token

api = Blueprint("api", __name__) 

@api.before_request
def load_user():
    load_user_from_token(request)

from . import errors, user, tags, colors 
