from flask import Blueprint, request 
from app.lib.decorators import load_user_from_token, owns_tag, owns_resource
from app.database import db_session


api = Blueprint("api", __name__) 

@api.before_request
def load_user():
    load_user_from_token(request)

def delete_models( model, body:dict, key: str):
    model_ids = request.json[key]
    if not model_ids: raise ValidationError("ids required")
    for id in model_ids :
        owns_resource(model, "resource_id")(lambda resource_id: None)(resource_id=id)
    [ db_session.delete(m)  for m in map(lambda id : model.query.get(id), model_ids)]
    db_session.commit() 
    

from . import errors, user, tags, colors 
