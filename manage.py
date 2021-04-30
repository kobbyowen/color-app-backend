from functools import wraps 
import os
import unittest
import click 
from flask import Blueprint
from app.database import create_all_tables, remove_all_tables
from app.lib.decorators import use_coverage
from config import basedir

database_commands = Blueprint("db", __name__)
test_commands = Blueprint("test", __name__)


def _create_dirs():
    if not os.path.exists("data") : os.mkdir("data")
    if not os.path.exists("tests/fixtures"): os.mkdir("tests/fixtures")
    

@database_commands.cli.command("create-all")
def create_tables():
    _create_dirs()
    create_all_tables()

@database_commands.cli.command("drop-all")
def remove_tables():
    remove_all_tables()

@test_commands.cli.command("all")
@use_coverage
def run_all_tests():
    _create_dirs()
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)

@test_commands.cli.command("coverage-test")
def run_coverage_tests():
    _create_dirs()
    cmd = """coverage run --omit 'venv/*'  -m unittest discover "tests" && coverage html -d coverage_html"""
    os.system(cmd)

@test_commands.cli.command("file")
@click.argument("filename")
@use_coverage
def test_file(filename):
    _create_dirs()
    tests = unittest.TestLoader().discover(
        "tests",
        pattern=f"*{filename}*")
    unittest.TextTestRunner(verbosity=2).run(tests)



