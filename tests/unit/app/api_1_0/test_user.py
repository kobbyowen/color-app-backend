from app.models import User, Tag, Color
from app.database import db_session
from tests import DefaultTestCase 
from tests import fetch, get_api_headers

def add_tags() :
    user = User.query.first() 
    tags  = [("tag1", "#ff0000", user.id),("tag2", "#0000ff", user.id), 
            ("tag3", "#00ff00", user.id) ]
    labels = ("name", "color", "user_id")
    db_session.add_all([Tag(**dict(zip(labels, args))) for args in tags])
    db_session.commit() 

def add_colors():
    user = User.query.first() 
    labels = ("name", "description", "rating", "code", "user_id")
    colors = [("Roses", "Bed color", 0, "#ff0000", user.id),
              ("Sunlight", "House Color", 1, "#ffff00", user.id),
              ("Blood", "Blood Of Jesus", 5,"#ff0000", user.id),
              ("Blue Gates", "Horror Movie", 2, "#0000ff", user.id),
              ("Green Leaf", "Favorite Tree", 3, "#00ff00", user.id),
              ("White Robe", "Heaven", 4, "#ffffff", user.id)
    ]
    db_session.add_all([Color(**dict(zip(labels, args))) for args in colors])
    db_session.commit() 



class TestUser(DefaultTestCase):
    def test_get_current_user (self):
        add_tags()
        add_colors()
        response = fetch( self.client,"/api/v1/user", "get", 
        headers=get_api_headers(User.query.first()) )
        body  = response.json
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("password", body)
        self.assertEqual(body["tagsCount"], 3)
        self.assertEqual(body["colorsCount"], 6)
        self.assertEqual(body["vicColorsCount"], 1)
        self.assertEqual(body["unratedColorsCount"], 1)
       
