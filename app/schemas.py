from flask import url_for, g
from marshmallow import Schema, fields, validate, validates , ValidationError, post_dump
from app.models import User, Color, Tag
import re 

def get_tags_data( ):
    tags_length = len(g.user.tags)
    tags_url = url_for("api.get_tags", _external=True)
    return tags_length, tags_url

def get_colors_data():
    colors_length = len(g.user.colors)
    colors_url = url_for("api.get_colors", _external=True)
    return colors_length, colors_url

def get_rated_colors_data(  rating, endpoint):
    length = len([color for color in g.user.colors if color.rating == rating ])
    url = url_for(endpoint, _external=True)
    return length, url 

def get_unrated_colors_data():
    return get_rated_colors_data( 0, "api.get_unrated_colors")

def get_starred_colors_data(  ):
    return get_rated_colors_data(1, "api.get_starred_colors")

def get_liked_colors_data( ):
    return get_rated_colors_data( 2, "api.get_liked_colors")

def get_loved_colors_data( ):
    return get_rated_colors_data( 3, "api.get_loved_colors")

def get_fav_colors_data(  ):
    return get_rated_colors_data( 4, "api.get_fav_colors")

def get_vic_colors_data( ):
    return get_rated_colors_data( 5, "api.get_vic_colors")



class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=8)) 
    verified = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True, data_key="createdAt") 
    modified_at = fields.DateTime(dump_only=True, data_key="modifiedAt") 


    @post_dump
    def add_urls( self, data, **kwargs):
        data["tagsCount"], data["tagsUrl"] =  get_tags_data() 
        data["colorsCount"], data["colorsUrl"]= get_colors_data()
        data["unratedColorsCount"], data["unratedColorsUrl"] = get_unrated_colors_data()
        data["starredColorsCount"], data["starredColorsUrl"] = get_starred_colors_data()
        data["likedColorsCount"], data["likedColorsUrl"] = get_liked_colors_data()
        data["lovedColorsCount"], data["lovedColorsUrl"] = get_loved_colors_data()
        data["favoriteColorsCount"], data["favoriteColorsUrl"] = get_fav_colors_data()
        data["vicColorsCount"], data["vicColorsUrl"] = get_vic_colors_data()

        return data 


    @validates('username')
    def validate_username(self, value):
        res = bool(re.search("\\s", value)) or bool(re.search("\\W", value))
        if res : raise ValidationError("username cannot contain spaces and punctuations")

    @validates('password')
    def validates_password(self, value):
        caps_found = re.search("[A-Z]", value)
        small_cases_found = re.search("[a-z]", value)
        digits_found = re.search("\\d", value)
        symbols_found = re.search("\\W", value)
        
        if not all([ bool(res) for res in ( caps_found, small_cases_found, digits_found, symbols_found)]):
            raise ValidationError("password must contain digits, punctuations and uppercase letters")



class TagSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(max=32, min=1))
    color = fields.Str(required=True, validate=validate.Length(max=7, min=7))
    created_at = fields.DateTime(dump_only=True, data_key="createdAt") 
    modified_at = fields.DateTime(dump_only=True, data_key="modifiedAt")

    @validates("name")
    def validate_name(self, value):
        if value[0].isdigit():
            raise ValidationError("tag name must not begin with a digit")            
        if re.search("\\W", value): 
            raise ValidationError("tag name must be alphanumeric characters only")

    @validates("color")
    def validate_color(self,value):
        if not value.startswith("#"):
            raise ValidationError("invalid color code")
        if re.search("[^a-f0-9]", value[1:], re.I):
            raise ValidationError("tag color code must be valid hex values")
    
    @post_dump
    def add_urls( self, data, **kwargs):
        id = data["id"]
        colors_length = len(Tag.query.get(id).colors ) 
        colors_url = url_for("api.get_colors_for_tag", tag_id=id) 
        data.update({
            "colorsCount" : colors_length, 
            "colorsUrl" : colors_url
        })

        return data 