import os
from app import create_app 
from app.database import db_session
from app.errors import ColorAppException
from app.lib.utils import Rest
from marshmallow import ValidationError 
from app.errors import RESOURCE_NOT_FOUND, VALIDATION_FAILED
from app.lib.utils import Rest


app = create_app(os.environ.get("FLASK_ENV") or "default")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)