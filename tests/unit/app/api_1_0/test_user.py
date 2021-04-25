from app.models import User, Tag, Color
from app.database import db_session
from tests import DefaultTestCase 
from tests import fetch, get_api_headers, add_tags , add_colors 


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
       
