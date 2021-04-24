import os 
from sqlalchemy import  create_engine, event 
from sqlalchemy.orm import scopped_session , session_maker 
from sqlite3 import Connection as SQLite3Connection
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base() 
config_name = os.environ.get("FLASK_ENV") or "default"
engine = create_engine(config[config_name].DATABASE_URI)
db_session = scoped_session(session_maker(autocommit=False, 
                                    autoflush=False , bind=engine))

@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


def create_all_tables():
    import app.models 
    app.models.CommonBase.metadata.create_all(bind=engine)

