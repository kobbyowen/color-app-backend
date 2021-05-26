from flask import g, request , url_for
from app.models import Color, ColorTags, Tag
from app.schemas import ColorSchema, TagSchema
from sqlalchemy.sql.expression import BinaryExpression
from app.lib.utils import Rest 
from app.lib.decorators import owns_color, owns_tag
from functools import partial 
from . import api , delete_colors
from app.errors import ColorAppException, DUPLICATE_RESOURCE, INSUFFICIENT_PERMISSION
from app.database import db_session


def _add_pagination_data( data:dict, page: int, size: int, count:int):
    data.update ({
        "next" : ((page + 1) * size) < count ,
        "prev" : page != 0 , 
        "count" : count  
    })
    return data 

def _get_color_tags(color_id:int, tag_ids:int):
    color_tags = [ColorTags.query.filter(
        ColorTags.color_id == color_id, ColorTags.tag_id == tag_id).first()
        for tag_id in tag_ids 
    ]
    assert(all(color_tags))
    return color_tags

def _remove_tags( color_id:int ,  tag_ids:list  ):
    if not tag_ids: return 
    color_tags = _get_color_tags(color_id, tag_ids)
    for color_tag in color_tags: db_session.delete(color_tag)
    db_session.commit() 


def _add_tags( color_id:int, tag_ids:list):
    if not tag_ids: return 
    color_tags = [ColorTags(color_id=color_id, tag_id=tag_id) for tag_id in tag_ids]
    for color_tag in color_tags: db_session.add(color_tag)
    db_session.commit() 


def _get_colors_helper(argslist, *expr) :
    if len(expr) and not all([isinstance(arg, BinaryExpression) for arg in expr]):
        raise TypeError("expr arguments must be of type 'BinaryExpression' ")
    filter_func = Color.query.filter
    user_filter_func = partial(filter_func, Color.user_id == g.user.id)
    count = user_filter_func(*expr).count() 
    page = int(argslist.get("page", 0))
    if page < 0 : page = 0
    size = int(argslist.get("size", count ))
    if size < 0 : size = 0 
    colors = user_filter_func(*expr).offset(page * size).limit(size).all() 
    data = ColorSchema().dump(colors, many=True)
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


@api.route("/color/<int:color_id>")
@owns_color
def get_color(color_id):
    color = Color.query.get(color_id)
    return Rest.success(data=ColorSchema().dump(color))


@api.route("/color/<int:color_id>/tags")
@owns_color
def get_color_tags(color_id):
    color_tags = Color.query.get(color_id).tags 
    tags = [Tag.query.get(color_tag.tag_id) for color_tag in color_tags]
    data = TagSchema().dumps(tags, many=True)
    return Rest.success(data= {"tags": data})

@api.route("/color/<int:color_id>/tags", methods=["PUT"])
@owns_color
def edit_color_tags(color_id):
    tag_ids = request.json["tag_ids"]
   
    # check tag ids if they exist and user owns them 
    for tag_id in tag_ids : 
        owns_tag(lambda tag_id: None)( tag_id = tag_id)
        
    existing_tags = Color.query.get(color_id).tags 
    existing_tag_ids = [existing_tag.tag_id for existing_tag in existing_tags]
    
    old_tag_ids = set(existing_tag_ids)
    new_tag_ids = set(tag_ids)

    _remove_tags( color_id,   list(old_tag_ids - new_tag_ids) )
    _add_tags( color_id, list( new_tag_ids - old_tag_ids))

    existing_tags = [Tag.query.get(color_tag.tag_id) for color_tag in Color.query.get(color_id).tags ]
    return Rest.success(data={"tags": TagSchema().dump(existing_tags, many=True)})

    
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
    color.user_id = g.user.id 
    db_session.add(color)
    db_session.commit() 
    return Rest.success(data=ColorSchema().dump(color), response_code=201, 
        **{"Location": url_for("api.get_color", color_id=color.id)}) 

@api.route("/color/<int:color_id>", methods=["PUT"])
@owns_color
def edit_colors(color_id):
    results = ColorSchema().load(request.json)
    _check_color_exists(color_id, results["name"], color_id)
    color = Color.query.get(color_id)
    color.name, color.code  = results["name"], results["code"]
    db_session.add(color)
    db_session.commit()
    return Rest.success(data=ColorSchema().dump(color))
    
@api.route("/color/<int:color_id>", methods=["DELETE"])
@owns_color
def remove_color(color_id):
    delete_colors({"color_ids": [color_id]}, "color_ids")
    return Rest.success() 

@api.route("/colors", methods=["DELETE"])
def remove_colors():
    delete_colors( request.json, "color_ids")
    return Rest.success()


