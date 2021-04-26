from flask import g, request 
from app.models import Color, ColorTags, Tag
from app.schemas import ColorSchema
from app.lib.utils import Rest 
from app.lib.decorators import owns_color
from . import api 


@api.route("/colors")
def get_colors():
    count = Color.query.filter(Color.user_id == g.user.id).count() 
    page = int(request.args.get("page", 0))
    size = int(request.args.get("size", count )) 
    colors = Color.query.filter(Color.user_id == g.user.id).offset(page * size).limit(size).all() 
    data = ColorSchema().dumps(colors, many=True)
    return Rest.success(data={"colors": data})



@api.route("/colors/<color_id>")
@owns_color
def get_color(color_id):
    color = Color.query.get(color_id)
    return Rest.success(data=ColorSchema().dump(color))


@api.route("/colors/<color_id>/tags")
@owns_color
def get_color_tags(color_id):
    tags = Color.query.get(color_id).tags 
    

@api.route("/colors/unrated")
def get_unrated_colors(): pass 


@api.route("/colors/starred")
def get_starred_colors(): pass 

@api.route("/colors/liked")
def get_liked_colors(): pass 

@api.route("/colors/loved")
def get_loved_colors(): pass 

@api.route("/colors/favorite")
def get_fav_colors(): pass

@api.route("/colors/vic")
def get_vic_colors():
    pass

@api.route("/colors", methods=["POST"])
def add_color():
    pass 

@api.route("/colors/<color_id>", methods=["PUT"])
def edit_colors(color_id):
    pass 

@api.route("/colors/<color_id>", methods=["DELETE"])
def remove_color(color_id):
    pass

@api.route("/colors", methods=["DELETE"])
def remove_colors():
    pass 


