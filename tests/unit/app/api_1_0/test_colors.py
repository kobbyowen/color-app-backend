from app.models import Color, Tag , ColorTags, User
from tests import DefaultTestCase, fetch, get_api_headers, add_colors, add_tags, get_api_headers
from random import sample 


def assign_tags_to_colors():
    color_ids = [ color.id for color in Color.query.all()]
    tag_ids = [tag.id for tag in Tag.query.all()]
    color_ids = sample(color_ids, 2)
    tag_ids = sample(tag_ids, 2)
    for color_id in color_ids:
        for tag_id in tag_ids :
            db_session.add(ColorTag(color_id=color_id, tag_id=tag_id))
    db_session.commit() 

class ColorTestCase( DefaultTestCase ):
    def setUp(self): 
        super().setUp() 
        add_tags()
        add_colors()
        assign_tags_to_colors() 

    def tearDown(self): 
        super().tearDown() 


class TestGetColorsEndpoint(ColorTestCase):
    def test_get_colors(self): 
        response = fetch(self.client, "/api/v1/colors", "get", 
            headers=get_api_headers(User.query.first()))
        colors = response.json["colors"]
        self.assertEqual(len(colors), Color.query.count())

    def test_get_colors_with_different_user_account(self):
        response = fetch(self.client, "/api/v1/colors", "get", 
            headers=get_api_headers(User.query.all()[1]))
        colors = response.json["colors"]
        self.assertEqual(len(colors), 0)

    def test_get_colors_pagination_with_small_size_arg(self): 
        response = fetch(self.client, "/api/v1/colors?page=0&size=2", "get", 
            headers=get_api_headers(User.query.first()))
        colors = response.json["colors"]
        self.assertEqual(len(colors), 2)
        self.assertTrue(response["next"])
        self.assertFalse(response["prev"])

    def test_get_colors_pagination_with_large_size_arg(self):
        pass 

    def test_get_tags_for_color(self): pass 
    def test_get_unstarred_colors(self): pass 
    def test_get_vic_colors(self): pass 

class TestAddColorsEndpoint(ColorTestCase):
    pass 

class TestEditColorsEndpoint(ColorTestCase):
    pass 

class TestDeleteColorsEndpoint(ColorTestCase):
    pass 
