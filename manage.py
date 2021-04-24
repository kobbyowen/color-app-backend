import click 
from run import app 
from flask.cli import AppGroup
from app.database import create_all_tables


database_cli = AppGroup("db")

@database_cli.command("create-all")
def create_tables():
    create_all_tables()

@database_cli.command("remove-all")
def remove_tables():
    pass 




