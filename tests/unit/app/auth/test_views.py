from app.models import User
from app.errors import VALIDATION_FAILED, LOGGED_OUT_TOKEN, INVALID_TOKEN
from tests import fetch , get_api_headers,  DefaultTestCase
from time import sleep 


class TestAuthLogin(DefaultTestCase):

    def test_login_with_no_username(self): 
        response = fetch(self.client, "/auth/login", "post", 
        {"password" : "sd32sdsd"}, get_api_headers())
        body = response.json
        self.assertEqual(body["errorCode"], VALIDATION_FAILED)

    def test_login_with_no_password(self):
        response = fetch(self.client, "/auth/login", "post", 
        {"username" : "tester"}, get_api_headers())
        body = response.get_json()
        self.assertEqual(body["errorCode"], VALIDATION_FAILED)
        
    def test_login_with_wrong_password(self): 
        response = fetch(self.client, "/auth/login", "post", 
        {"username" : "tester" , "password": "yt23-231DsK"}, get_api_headers())
        body = response.get_json() 
        self.assertEqual(body["errorCode"], VALIDATION_FAILED)

    def test_login_with_wrong_username(self): 
        response = fetch(self.client, "/auth/login", "post", 
        {"username" : "testerwrong" , "password": "yt23-231qsK"},get_api_headers())
        body = response.get_json() 
        self.assertEqual(body["errorCode"], VALIDATION_FAILED)

    def test_login_with_correct_credentials(self):  
        response = fetch(self.client, "/auth/login", "post", 
        {"username" : "tester" , "password": "yt23-231qsK"}, get_api_headers())
        body = response.get_json() 
        self.assertEqual(body["errorCode"], 0)
        self.assertEqual(response.status_code, 200)
        


class TestAuthRegister(DefaultTestCase):
    
    def test_register_with_verify_password_wrong(self):
        response = fetch(self.client, "/auth/register", "post", 
        {"username" : "tester3" , "password": "yt23-231DsK", "verifyPassword":"yt23-231DsM" },
         get_api_headers())
        body = response.get_json() 
        self.assertEqual(body["errorCode"], VALIDATION_FAILED)

    def test_register_with_password_length_less_than_8(self): 
        response = fetch(self.client, "/auth/register", "post", 
        {"username" : "tester3" , "password": "31DsK", "verifyPassword":"31DsK" },
         get_api_headers())
        body = response.get_json() 
        self.assertEqual(body["errorCode"], VALIDATION_FAILED)

    def test_register_with_password_without_symbols(self): 
        response = fetch(self.client, "/auth/register", "post", 
        {"username" : "tester3" , "password": "yt23231DsK", "verifyPassword":"yt23231DsK" },
         get_api_headers())
        body = response.get_json() 
        self.assertEqual(body["errorCode"], VALIDATION_FAILED)
 
    def test_register_with_password_without_uppercase(self): 
        response = fetch(self.client, "/auth/register", "post", 
        {"username" : "tester3" , "password": "yt23-231DsK".lower(), 
        "verifyPassword":"yt23-231DsK".lower() },
         get_api_headers())
        body = response.get_json() 
        self.assertEqual(body["errorCode"], VALIDATION_FAILED)

    def test_register_with_password_without_numbers(self): 
        response = fetch(self.client, "/auth/register", "post", 
        {"username" : "tester3" , "password": "ytdmt?DsK", "verifyPassword":"ytdmt?DsK" },
         get_api_headers())
        body = response.get_json() 
        self.assertEqual(body["errorCode"], VALIDATION_FAILED)

    def test_register_with_password_without_lower_alphabets(self): 
        response = fetch(self.client, "/auth/register", "post", 
        {"username" : "tester3" , "password": "yt23-231DsK".upper(), "verifyPassword":"yt23-231DsK".upper() },
         get_api_headers())
        body = response.get_json() 
        self.assertEqual(body["errorCode"], VALIDATION_FAILED)
 
    def test_register_with_username_with_symbols(self): 
        response = fetch(self.client, "/auth/register", "post", 
        {"username" : "tester-3" , "password": "yt23-231DsK", "verifyPassword":"yt23-231DsK" },
         get_api_headers())
        body = response.get_json() 
        self.assertEqual(body["errorCode"], VALIDATION_FAILED)

    def test_register_with_username_with_spaces(self): 
        response = fetch(self.client, "/auth/register", "post", 
        {"username" : "tester 3" , "password": "yt23-231DsK", "verifyPassword":"yt23-231DsK" },
         get_api_headers())
        body = response.get_json() 
        self.assertEqual(body["errorCode"], VALIDATION_FAILED) 
    
    def test_register_with_username_that_exists(self): 
        response = fetch(self.client, "/auth/register", "post", 
        {"username" : "tester" , "password": "yt23-231DsK", "verifyPassword":"yt23-231DsK" },
         get_api_headers())
        body = response.get_json() 
        self.assertEqual(body["errorCode"], VALIDATION_FAILED)

    def test_register_with_correct_details(self): 
        response = fetch(self.client, "/auth/register", "post", 
        {"username" : "tester_3" , "password": "yt23-231DsK", "verifyPassword":"yt23-231DsK" },
         get_api_headers())
        body = response.get_json() 
        self.assertEqual(body["errorCode"],0)
    

class TestAuthLogout(DefaultTestCase):
    def logout_user(self): 
        response = fetch(self.client, "/auth/logout", "get", 
        headers=get_api_headers(User.query.first()))
        body = response.get_json() 
        self.assertEqual(body["errorCode"],0)
        self.assertEqual(response.status_code,200)

    def access_protected_route_with_logged_out_token(self):
        headers=get_api_headers(User.query.first())
        old_token = headers["Authorization"]
        response = fetch(self.client, "/auth/logout", "get",  headers=headers)
        body = response.json() 
        self.assertEqual(body["errorCode"],0)
        self.assertEqual(response.status_code,200)

        headers=get_api_headers(User.query.first())
        headers["Authorization"] = old_token
        # logout is a protected endpoint
        response = fetch(self.client, "/auth/logout", "get",  headers=headers)
        self.assertEqual(body["errorCode"], LOGGED_OUT_TOKEN)
        self.assertEqual(response.status_code, 400)


class TestAuthVerifyUser(DefaultTestCase):
    def test_verify_user(self): 
        headers=get_api_headers(User.query.filter(User.verified == False).first())
        response = fetch(self.client, "/auth/verify", "put",  headers=headers)
        body = response.get_json()
        self.assertEqual(body["errorCode"], 0)
        self.assertTrue(User.query.filter(User.verified == False).first() is None)



class TestAuthNewToken(DefaultTestCase):

    def test_get_new_token_without_token(self): 
        headers=get_api_headers(User.query.first())
        response = fetch(self.client, "/auth/new-token", "post",  
        data = {"key": "unknown"}, headers=headers)
        body = response.get_json() 
        self.assertEqual(body["errorCode"], VALIDATION_FAILED)
        
    def test_get_new_token_with_invalid_token(self): 
        response = fetch(self.client, "/auth/new-token", "post",  
        data = {"token": "some-token"}, headers=get_api_headers())
        body = response.get_json() 
        self.assertEqual(body["errorCode"], INVALID_TOKEN)

    def test_get_new_token_with_valid_token(self): 
        headers = headers=get_api_headers(User.query.filter(User.username == "tester").first())
        token = headers["Authorization"]
        response = fetch(self.client, "/auth/new-token", "post",  
        data = {"token": token}, headers=headers)
        body = response.get_json() 
        self.assertEqual(body["errorCode"], 0)

    def test_get_new_token_with_expired_token(self): 
        headers = headers=get_api_headers(User.query.filter(User.username == "tester").first(), 1)
        token = headers["Authorization"]
        sleep(1) # be sure to expire the token
        response = fetch(self.client, "/auth/new-token", "post",  
        data = {"token": token}, headers=headers)
        body = response.get_json() 
        self.assertEqual(body["errorCode"], 0)
