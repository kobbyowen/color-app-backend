from flask import g
from . import api
from app.schemas import UserSchema
from app.lib.utils import Rest

@api.route("/user")
def get_current_user():
    result = UserSchema().dump(g.user)
    return Rest.success(data=result)


