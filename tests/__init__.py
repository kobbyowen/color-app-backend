import json
from app import create_app
from app.database import create_all_tables, remove_all_tables, db_session
from unittest import TestCase
from app.database import  db_session
from app.models import User 

def add_users():
    userA = User(username="tester", password="yt23-231qsK")
    userB = User(username="tester2", password="23-231.KJvty") 
    userA.verified = True 
    db_session.add_all([userA, userB])
    db_session.commit() 

class DefaultTestCase(TestCase):
    def setUp(self):
        self.app, self.client = before_test_run(add_users)
        self.app_context = self.app.app_context() 
        self.app_context.push() 

    def tearDown(self):
        after_test_run() 
        self.app_context.pop() 



def fetch(  client, route:str , method:str ="get", data:dict = None, headers:dict = None):
        func = None 
        if method.lower() == "get": func = client.get 
        elif method.lower() == "post" : func = client.post 
        elif method.lower() == "put" : func = client.put 
        elif method.lower() == "delete": func = client.delete 
        else : raise ValueError(f'{method} is invalid')
        arguments = {} 
        if data : arguments["data"] = json.dumps(data)
        if headers: arguments["headers"] = headers
      
        response = func( route, **arguments)
        return response 


def get_api_headers(user=None, expire=None):
        return {
            'Authorization': "JWT " + user.generate_token(expire=expire) if user else "No-Auth",
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }    


def before_test_run ( pre_run_func=lambda f=None: f , create_tables=True):
    app =  create_app("testing")
    if create_tables : create_all_tables()
    client = app.test_client(use_cookies=True)
    pre_run_func() 
    return app,  client 

def after_test_run ( post_run_func=lambda f=None: f , remove_tables=True):
    if remove_tables:
        remove_all_tables()
    post_run_func() 

