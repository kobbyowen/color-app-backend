import functools
from flask import Blueprint, request 
from app.lib.decorators import load_user_from_token, owns_tag, owns_resource
from app.database import db_session
from app.models import Color, Tag

api = Blueprint("api", __name__) 

@api.before_request
def load_user():
    if request.method.lower() == "options": return 
    load_user_from_token(request)

def delete_color_side_effects(id):
    color = Color.query.get(id)
    tags = color.tags 
    [db_session.delete(tag) for tag in tags ]
    db_session.commit() 

def delete_tag_side_effects(id):
    tag = Tag.query.get(id)
    colors = tag.colors 
    [db_session.delete(color) for color in colors ]
    db_session.commit() 


def delete_models( model, body:dict, key: str):
    model_ids = body[key]
    if not model_ids: raise ValidationError("ids required")
    for id in model_ids :
        owns_resource(model, "resource_id")(lambda resource_id: None)(resource_id=id)
        if model is Color: delete_color_side_effects(id) 
        if model is Tag : delete_tag_side_effects(id)
    [ db_session.delete(m)  for m in map(lambda id : model.query.get(id), model_ids)]
    db_session.commit() 
    
delete_colors = functools.partial(delete_models, Color)
delete_tags = functools.partial(delete_models, Tag)

from . import errors, user, tags, colors 
