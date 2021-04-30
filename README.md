# color-app-backend
A color organizing app in Flask

Uses Flask, SQLAlchemy and Marshmallow.
# I DIDNT USE FLASK-SQLALCHEMY because I dont like it!!!!!! (PRACTICE LOOSE COUPLING )
# I DIDNT USE FLASK-MARSHMALLOW because I dont like it!!!!!! (PRACTICE LOOSE COUPLING )

Easy Code For Flask Beginners To Study

Incorporates Tests And Coverage 

This is a simple App. 
It allow users to organize colors by adding , removing and editting the colors.
Users can add tags to colors

## Setting Up 
```bash
python -m venv venv 
source venv/bin/activate 
pip install -r requirements.txt
#create database and all tables 
flask db create-all 
```
## Run The App 

```bash
export FLASK_ENV=development 
export FLASK_APP=run.py 
flask run 
```

## Running Tests 
### Run Tests In A Particular File

```bash
export FLASK_ENV=development 
export FLASK_APP=run.py 
flask test file [test file name]
```
### Run All Tests

```bash 
# use set instead of export on windows
export FLASK_ENV=development 
export FLASK_APP=run.py 
flask test all
```

### Run Coverage Tests 
```bash 
export FLASK_ENV=development 
export FLASK_APP=run.py 
flask test coverage-test
```


