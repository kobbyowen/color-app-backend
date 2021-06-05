from datetime import datetime
from flask import request, abort, g, url_for
from . import auth
from app.models import User, LoggedOutToken
from app.schemas import UserSchema
from app.lib.utils import Rest
from app.database import db_session
from app.lib.decorators import protected
from marshmallow import ValidationError
 

def issue_new_token(user: User, expire: int = 3600):
    data = {
        "token": user.generate_token(expire=expire),
        "expires": expire,
        "issuedAt": datetime.utcnow(),
        "userUrl": url_for("api.get_current_user", _external=True),
        "verified": user.verified
    }
    return data


@auth.route("/login", methods=["POST"])
def login():
    body = request.json
    if "password" not in body or "username" not in body:
        raise ValidationError("username and password required to login")
    user = User.query.filter(User.username == body["username"]).first()
    if not (user and user.verify_password(body["password"])):
        raise ValidationError("username or password is incorrect")
    data = issue_new_token(user)
    return Rest.success(data=data)


@auth.route("/register",  methods=["POST"])
def register():
    body = request.json
    if body["verifyPassword"] != body["password"]:
        raise ValidationError("passwords do not match")
    del body["verifyPassword"]
    results = UserSchema().load(body)
    user_exists = User.query.filter(
        User.username == results["username"]).first() is not None
    if user_exists:
        raise ValidationError("username already taken")
    user = User(results["username"], results["password"])
    db_session.add(user)
    db_session.commit()
    data = issue_new_token(user)
    return Rest.success(data=data)


@auth.route("/new-token",  methods=["POST"])
def get_new_token():
    old_token = request.json.get("token")
    if not old_token:
        raise ValidationError("token is required")
    user = User.verify_token(old_token.lstrip("JWT "), False)
    data = issue_new_token(user)
    return Rest.success(data=data)


@auth.route("/verify", methods=["PUT"])
@protected
def verify_account():
    user = g.user
    user.verified = True
    db_session.add(user)
    db_session.commit()
    return Rest.success()


@auth.route("/logout")
@protected
def logout():
    token = request.headers.get("Authorization").lstrip("JWT ")
    db_session.add(LoggedOutToken(token=token))
    db_session.commit()
    return Rest.success()
