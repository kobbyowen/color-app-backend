import os 
from sqlalchemy import  create_engine, event ,inspect
from sqlalchemy.orm import  sessionmaker , scoped_session
from sqlite3 import Connection as SQLite3Connection
from sqlalchemy.ext.declarative import declarative_base
from config import config 


config_name = os.environ.get("FLASK_ENV") or "default"
engine = create_engine(config[config_name].DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False, 
                                    autoflush=False , bind=engine))
Base = declarative_base() 
Base.query = db_session.query_property()


@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

def table_exists(engine,name):
    ins = inspect(engine)
    ret =ins.dialect.has_table(engine.connect(),name)
    return ret

def create_all_tables():
    import app.models 
    if table_exists(engine, "users") : 
        return 
    app.models.Base.metadata.create_all(bind=engine)


def remove_all_tables():
    import app.models 
    if not table_exists(engine, "users"): return 
    app.models.Base.metadata.drop_all(bind=engine)