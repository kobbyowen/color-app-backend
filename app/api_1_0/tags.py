from . import api 
from app.models import Tag 
from app.schemas import TagSchema
from flask import g , request, url_for 
from app.lib.utils import Rest
from app.database import db_session
from app.lib.decorators import owns_resource
from app.errors import ColorAppException, DUPLICATE_RESOURCE
from marshmallow import ValidationError 

@api.route("/tags")
def get_tags():
    tags = Tag.query.filter(Tag.user_id == g.user.id ).all() 
    data = TagSchema().dump(tags, many=True)
    return Rest.success(data={"tags": data})


@api.route("/tags", methods=["POST"])
def add_tag():
    results = TagSchema().load(request.json)
    tag = Tag.query.filter(Tag.name == results["name"], Tag.user_id == g.user.id).first() 
    if tag: raise ColorAppException(DUPLICATE_RESOURCE, "a tag with same name already exist",400)
    tag = Tag(**results)
    tag.user_id = g.user.id 
    db_session.add(tag)
    db_session.commit() 
    return Rest.success(data=TagSchema().dump(tag), response_code=201, 
    headers={"Location": url_for("api.get_tag_details", tag_id=tag.id)})


@api.route("/tag/<int:tag_id>")
@owns_resource(Tag, "tag_id")
def get_tag_details(tag_id):
    return Rest.success(data=TagSchema().dump(Tag.query.get(tag_id)))


@api.route("/tag/<int:tag_id>", methods=["PUT"])
@owns_resource(Tag, "tag_id")
def get_edit_tag(tag_id):
    body = request.json
    tag = Tag.query.get(tag_id) 
    results = TagSchema().load(body)
    tag_check = Tag.query.filter(Tag.id!=tag_id, Tag.name==results["name"],
             Tag.user_id == g.user.id).first()
    if tag_check: raise ColorAppException(DUPLICATE_RESOURCE, "a tag with same name already exist",400) 
    tag.name = results["name"]
    tag.color = results["color"]
    db_session.add(tag)
    db_session.commit() 
    data=TagSchema().dump(tag)
    return Rest.success(data=data)

    
@api.route("/tag/<int:tag_id>", methods=["DELETE"])
@owns_resource(Tag, "tag_id")
def remove_tag(tag_id):
    tag = Tag.query.get(tag_id)
    db_session.delete(tag) 
    db_session.commit() 
    return Rest.success()


@api.route("/tags", methods=["DELETE"])
def remove_tags():
    tag_ids = request.json.get("tag_ids")
    if not tag_ids: raise ValidationError("tag ids required")
    for tag_id in tag_ids :
        owns_resource(Tag, "tag_id")(lambda tag_id: None)(tag_id=tag_id)
    map(lambda tag: db_session.delete(tag) , map(lambda id : Tag.query.get(id), tag_ids))
    db_session.commit() 
    return Rest.success()

# @api.route("/tag/<int:tag_id>/colors")
# def get_colors_for_tag(tag_id):
#     colors = Tag.query.get(tag_id).colors 
#     colors_length= len(colors)
#     # raise value error if value cannot be converted to integer
#     # allow it and catch it later 
#     count = int(request.args.get("per_page",  20))
#     if count > colors_length : count = colors_length

#     start = int(request.args.get("start", 0))
#     if start < 0 : start = 0 
#     if start > colors_length : start = colors_length

#     colors = colors[start: start+count] 
#     prev = start != 0 
#     prevCount = start 
#     next = len(colors) + start < colors_length 
#     nextCount = colors_length - (len(colors) + start)
