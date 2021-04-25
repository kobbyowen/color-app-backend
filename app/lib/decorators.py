from functools import wraps
import os 
from flask import abort , g , Request, request
from app.models import User, LoggedOutToken
from app.lib.utils import Rest 
from coverage import coverage, Coverage , misc
from app.errors import ColorAppException, NO_TOKEN_PROVIDED,EXPIRED_TOKEN, INVALID_TOKEN, LOGGED_OUT_TOKEN 
import jwt 

def load_user_from_token( request : Request ):
    token = request.headers.get("Authorization") 

    if not token:  raise ColorAppException(NO_TOKEN_PROVIDED, "Please provide a token", 400)
    
    token = token.lstrip("JWT ")
    
    user = None 
    try: user = User.verify_token(token)
    except jwt.exceptions.ExpiredSignatureError: raise ColorAppException( EXPIRED_TOKEN, "token has expired", 400)
    except jwt.exceptions.InvalidTokenError: raise ColorAppException( INVALID_TOKEN, "token is invalid", 400)
    assert(user is not None )

    logged_out = LoggedOutToken.query.filter(LoggedOutToken.token==token).first() is not None 
    if logged_out: raise ColorAppException(LOGGED_OUT_TOKEN, "token cannot be used", 400) 
    
    g.user = user 


def protected(f):
    @wraps(f) 
    def dec ( *args, **kwargs):
        load_user_from_token(request)
        return f(*args, **kwargs)
    return dec 



def generate_coverage_report( cov: Coverage ):
    try:
        cov.report()
        basename = os.path.abspath(os.path.dirname(__file__))
        basedir =  f"{basename.rstrip('/')}/tests/fixtures/coverage"
        os.makedirs(basedir, exist_ok=True)
        covdir = os.path.join(basedir)
        cov.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        cov.erase()
    except misc.CoverageException:
        print("Coverage could not be processed")


def use_coverage(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        #check if we are testing a particular file or all files 
        filename = kwargs.get("filename") or "*"
        filename = filename.lstrip("test_")

        cov = coverage(branch=True, include=f"app/*{filename}*")
        cov.start() 
        res = f(*args, **kwargs) 
        cov.stop() 
        generate_coverage_report( cov )
        return res 
    return decorated_func
