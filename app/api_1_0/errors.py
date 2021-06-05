from . import api
from app.lib.utils import Rest
from app.errors import MALFORMED_URL


@api.errorhandler(ValueError)
def malformed_url(err):
    return Rest.error(code=MALFORMED_URL, message="URL query parameters is invalid")
