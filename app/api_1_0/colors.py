from flask import g, request 
from app.models import Color, ColorTags, Tag
from app.schemas import ColorSchema
from sqlalchemy.sql.elements import BinaryExpression
from app.lib.utils import Rest 
from app.lib.decorators import owns_color
from functools import partial 
from . import api , delete_models
from app.errors import ColorAppException, DUPLICATE_RESOURCE


def _add_pagination_data( data:dict, page: int, size: int, count:int):
    data.update ({
        "next" : (page * size) < count ,
        "prev" : page != 0 , 
        "count" : count  
    })
    return data 

def _get_colors_helper(argslist, *expr) :
    if len(expr) and not all([isinstance(arg, BinaryExpression) for arg in expr]):
        raise TypeError("expr arguments must be of type 'BinaryExpression ")
    filter_func = Color.query.filter
    user_filter_func = partial(filter_func, Color.user_id == g.user.id)
    count = user_filter_func(*expr).count() 
    page = int(argslist.get("page", 0))
    size = int(argslist.get("size", count ))
    colors = user_filter_func(*expr).offset(page * size).limit(size).all() 
    data = ColorSchema().dumps(colors, many=True)
    data = _add_pagination_data( {"colors" : data}, page, size, count)
    return data 

def _check_color_exists(  name, id=-1 ):
    color_exists = Color.query.filter(
        Color.id!= id, Color.name==name, Color.user_id == g.user.id
    ).first() is not None 
    if color_exists:
        raise ColorAppException(DUPLICATE_RESOURCE, "a color with same name exists")

@api.route("/colors")
def get_colors():
    data = _get_colors_helper(request.args)
    return Rest.success(data=data)


@api.route("/colors/<color_id>")
@owns_color
def get_color(color_id):
    color = Color.query.get(color_id)
    return Rest.success(data=ColorSchema().dump(color))


@api.route("/colors/<color_id>/tags")
@owns_color
def get_color_tags(color_id):
    tags = Color.query.get(color_id).tags 
    

@api.route("/colors/<color_id>/tags", method=["PUT"])
@owns_color
def get_color_tags(color_id):
    tags = Color.query.get(color_id).tags 
   
@api.route("/colors/unrated")
def get_unrated_colors(): 
    data = _get_colors_helper(request.args, Color.rating == 0)
    return Rest.success(data=data)


@api.route("/colors/starred")
def get_starred_colors(): 
    data = _get_colors_helper(request.args, Color.rating == 1)
    return Rest.success(data=data)


@api.route("/colors/liked")
def get_liked_colors(): 
    data = _get_colors_helper(request.args, Color.rating == 2)
    return Rest.success(data=data)

@api.route("/colors/loved")
def get_loved_colors(): 
    data = _get_colors_helper(request.args, Color.rating == 3)
    return Rest.success(data=data)

@api.route("/colors/favorite")
def get_fav_colors(): 
    data = _get_colors_helper(request.args, Color.rating == 4)
    return Rest.success(data=data)

@api.route("/colors/vic")
def get_vic_colors():
    data = _get_colors_helper(request.args, Color.rating == 5)
    return Rest.success(data=data)

@api.route("/colors", methods=["POST"])
def add_color():
    results = ColorSchema().load(request.json)
    _check_color_exists( results["name"])
    color = Color(**results)
    db_session.add(color)
    db_session.commit() 
    return Rest.success(data=ColorSchema().dump(color), response_code=201, 
        **{"Location": url_for("api.get_color", color_id=color.id)}) 

@api.route("/colors/<color_id>", methods=["PUT"])
@owns_color
def edit_colors(color_id):
    results = ColorSchema().load(request.json)
    _check_color_exists(color_id, results["name"], color_id)
    color = Color.query.get(color_id)
    color.name, color.code  = results["name"], results["code"]
    db_session.add(color)
    db_session.commit()
    return Rest.success(data=ColorSchema().dump(color))
    
@api.route("/colors/<color_id>", methods=["DELETE"])
@owns_color
def remove_color(color_id):
    db_session.delete(Color.query.get(color_id))
    db_session.commit() 
    return Rest.success() 

@api.route("/colors", methods=["DELETE"])
def remove_colors():
    delete_models(Color, request.json, "colors_id")
    return Rest.success()


