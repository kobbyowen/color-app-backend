import os
from app import create_app 
from app.database import db_session

app = create_app(os.environ.get("FLASK_ENV") or "default")

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove() 

    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)