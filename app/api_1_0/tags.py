from . import api, delete_tags
from app.models import Tag, Color
from app.schemas import TagSchema, ColorSchema
from flask import g, request, url_for
from app.lib.utils import Rest
from app.database import db_session
from app.lib.decorators import owns_tag
from app.errors import ColorAppException, DUPLICATE_RESOURCE
from marshmallow import ValidationError


def _check_tag_exists(name, id=-1):
    tag_check = Tag.query.filter(
        Tag.id != id, Tag.name == name, Tag.user_id == g.user.id).first()
    if tag_check:
        raise ColorAppException(
            DUPLICATE_RESOURCE, "a tag with same name already exist", 400)


@api.route("/tags")
def get_tags():
    tags = Tag.query.filter(Tag.user_id == g.user.id).all()
    data = TagSchema().dump(tags, many=True)
    return Rest.success(data={"tags": data})


@api.route("/tags", methods=["POST"])
def add_tag():
    results = TagSchema().load(request.json)
    _check_tag_exists(results["name"])
    tag = Tag(**results)
    tag.user_id = g.user.id
    db_session.add(tag)
    db_session.commit()
    return Rest.success(data=TagSchema().dump(tag), response_code=201,
                        headers={"Location": url_for("api.get_tag_details", tag_id=tag.id, _external=True)})


@api.route("/tag/<int:tag_id>")
@owns_tag
def get_tag_details(tag_id):
    return Rest.success(data=TagSchema().dump(Tag.query.get(tag_id)))


@api.route("/tag/<int:tag_id>", methods=["PUT"])
@owns_tag
def get_edit_tag(tag_id):
    body = request.json
    tag = Tag.query.get(tag_id)
    results = TagSchema().load(body)
    _check_tag_exists(results["name"], tag_id)
    tag.name, tag.color = results["name"], results["color"]
    db_session.add(tag)
    db_session.commit()
    return Rest.success(data=TagSchema().dump(tag))


@api.route("/tag/<int:tag_id>", methods=["DELETE"])
@owns_tag
def remove_tag(tag_id):
    delete_tags({"tag_ids": [tag_id]}, "tag_ids")
    return Rest.success()


@api.route("/tags", methods=["DELETE"])
def remove_tags():
    delete_tags(request.json, "tag_ids")
    return Rest.success()


@api.route("/tag/<int:tag_id>/colors")
@owns_tag
def get_colors_for_tag(tag_id):
    color_tags = Tag.query.get(tag_id).colors
    colors = [Color.query.get(color_tag.color_id) for color_tag in color_tags]
    return Rest.success(data={"colors": ColorSchema().dump(colors, many=True)})
