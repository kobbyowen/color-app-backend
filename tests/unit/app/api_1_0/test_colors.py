from app.models import Color, Tag , ColorTags, User
from tests import DefaultTestCase, fetch, get_api_headers, add_colors, add_tags, get_api_headers
from random import sample 
from app.database import db_session
from app.errors import MALFORMED_URL, VALIDATION_FAILED

def assign_tags_to_colors():
    color_ids = [ color.id for color in Color.query.all()]
    tag_ids = [tag.id for tag in Tag.query.all()]
    color_ids = sample(color_ids, 2)
    tag_ids = sample(tag_ids, 2)
    for color_id in color_ids:
        for tag_id in tag_ids :
            db_session.add(ColorTags(color_id=color_id, tag_id=tag_id))
    db_session.commit() 

class ColorTestCase( DefaultTestCase ):
    def setUp(self): 
        super().setUp() 
        add_tags()
        add_colors()
        assign_tags_to_colors() 

    def tearDown(self): 
        super().tearDown() 


# class TestGetColorsEndpoint(ColorTestCase):
#     def test_get_colors(self): 
#         response = fetch(self.client, "/api/v1/colors", "get", 
#             headers=get_api_headers(User.query.first()))
#         colors = response.json["colors"]
#         self.assertEqual(len(colors), Color.query.count())

#     def test_get_colors_with_different_user_account(self):
#         response = fetch(self.client, "/api/v1/colors", "get", 
#             headers=get_api_headers(User.query.all()[1]))
#         colors = response.json["colors"]
#         self.assertEqual(len(colors), 0)

#     def test_get_colors_pagination_with_small_size_arg(self): 
#         response = fetch(self.client, "/api/v1/colors?page=0&size=2", "get", 
#             headers=get_api_headers(User.query.first()))
#         colors = response.json["colors"]
#         self.assertEqual(len(colors), 2)
#         self.assertTrue(response.json["next"])
#         self.assertFalse(response.json["prev"])

#     def test_get_colors_pagination_with_large_size_arg(self):
#         response = fetch(self.client, "/api/v1/colors?page=0&size=100", "get", 
#             headers=get_api_headers(User.query.first()))
#         colors = response.json["colors"]
#         self.assertEqual(len(colors), Color.query.filter(Color.user_id==User.query.first().id).count())
#         self.assertFalse(response.json["next"])
#         self.assertFalse(response.json["prev"])

#     def test_get_colors_pagination_with_larger_page_arg(self):
#         response = fetch(self.client, "/api/v1/colors?page=5&size=100", "get", 
#             headers=get_api_headers(User.query.first()))
#         colors = response.json["colors"]
#         self.assertEqual(len(colors), 0)
#         self.assertFalse(response.json["next"])
#         self.assertTrue(response.json["prev"])

#     def test_get_colors_pagination_with_negative_page_arg(self):
#         response = fetch(self.client, "/api/v1/colors?page=-1&size=100", "get", 
#             headers=get_api_headers(User.query.first()))
#         colors = response.json["colors"]
#         self.assertEqual(len(colors), 6)
#         self.assertFalse(response.json["next"])
#         self.assertFalse(response.json["prev"])

    
#     def test_get_colors_pagination_with_negative_size_arg(self):
#         response = fetch(self.client, "/api/v1/colors?page=0&size=-10", "get", 
#             headers=get_api_headers(User.query.first()))
#         colors = response.json["colors"]
#         self.assertEqual(len(colors), 0)
#         self.assertTrue(response.json["next"])
#         self.assertFalse(response.json["prev"])

#     def test_get_colors_with_invalid_args(self):
#         response = fetch(self.client, "/api/v1/colors?page=a&size=-10", "get", 
#             headers=get_api_headers(User.query.first()))
#         code = response.json["code"]
#         self.assertEqual(code, MALFORMED_URL)
#         response = fetch(self.client, "/api/v1/colors?page=0&size=b", "get", 
#             headers=get_api_headers(User.query.first()))
#         code = response.json["code"]
#         self.assertEqual(code, MALFORMED_URL)

#     def test_get_tags_for_color(self): 
#         color_id = Color.query.first().id 
#         response = fetch(self.client, f"/api/v1/color/{color_id}/tags", "get", 
#             headers=get_api_headers(User.query.first()))
#         self.assertIn("tags", response.json)

#     def test_get_unrated_colors(self): 
#         user = User.query.first()
#         response = fetch(self.client, f"/api/v1/colors/unrated", "get", 
#             headers=get_api_headers(user))
#         colors = response.json["colors"]
#         self.assertEqual(len(colors), Color.query.filter(Color.user_id == user.id, Color.rating==0).count())
 

#     def test_get_vic_colors(self): 
#         user = User.query.first()
#         response = fetch(self.client, f"/api/v1/colors/vic", "get", 
#             headers=get_api_headers(user))
#         colors = response.json["colors"]
#         self.assertEqual(len(colors), Color.query.filter(Color.user_id == user.id, Color.rating==5).count())

# class TestAddColorsEndpoint(ColorTestCase):
#     def test_add_color_with_invalid_name(self): 
#         invalid_names = ["invalid-name-1", "3invalidname", "some#here"]
#         for invalid_name in invalid_names:
#             response = fetch(self.client, "/api/v1/colors", "post", 
#             headers=get_api_headers(User.query.first()),
#             data={"name": invalid_name, "code": "#ffffff", "rating": 1, "description": "help"}
#             )
#             self.assertEqual(response.json["code"], VALIDATION_FAILED)

#     def test_add_color_with_invalid_rating(self): 
#         invalid_rates = [6, -1]
#         for invalid_rate in invalid_rates:
#             response = fetch(self.client, "/api/v1/colors", "post", 
#             headers=get_api_headers(User.query.first()),
#             data={"name": "kobby", "code": "#ffffff", "rating": invalid_rate, "description": "help"}
#             )
#             self.assertEqual(response.json["code"], VALIDATION_FAILED)

#     def test_add_color_with_invalid_code(self): 
#         invalid_codes = ["ffffff", "#123jff"]
#         for invalid_code in invalid_codes:
#             response = fetch(self.client, "/api/v1/colors", "post", 
#             headers=get_api_headers(User.query.first()),
#             data={"name": "kobby", "code": invalid_code, "rating": 3, "description": "help"}
#             )
#             self.assertEqual(response.json["code"], VALIDATION_FAILED)


#     def test_add_valid_color(self): 
#         user = User.query.first()
#         old_color_count = Color.query.filter(Color.user_id == user.id).count() 

#         response = fetch(self.client, "/api/v1/colors", "post", 
#             headers=get_api_headers(user),
#             data={"name": "kobby", "code": "#ddddee", "rating": 3, "description": "help"}
#         )
#         new_color_count = Color.query.filter(Color.user_id == user.id).count() 
#         self.assertEqual( new_color_count, old_color_count + 1)
#         self.assertEqual(response.status_code, 201)

class TestEditColorsEndpoint(ColorTestCase):
    pass 

class TestDeleteColorsEndpoint(ColorTestCase):
    def test_remove_color_that_user_doesnt_own(self): 
        color = Color.query.first() 
        user = User.query.filter(User.id != color.user_id).first() 
        assert(user is not None)
        response = fetch(self.client, f"/api/v1/color/{color.id}", "delete", 
        headers=get_api_headers(user))
        self.assertEqual(response.status_code , 403)


    def test_remove_color_that_user_own(self): 
        color = Color.query.first() 
        user = User.query.get(color.user_id) 
        old_color_count = Color.query.filter(Color.user_id == user.id).count()
        assert(user is not None)
        response = fetch(self.client, f"/api/v1/color/{color.id}", "delete", 
        headers=get_api_headers(user))
        new_color_count = Color.query.filter(Color.user_id == user.id).count()
        self.assertEqual(response.status_code , 200)
        self.assertEqual(new_color_count, old_color_count - 1)


    def test_remove_colors_with_one_invalid_id(self): 
        color = Color.query.first() 
        user = User.query.get(color.user_id) 
        old_color_count = Color.query.filter(Color.user_id == user.id).count()
        assert(user is not None)
        response = fetch(self.client, f"/api/v1/colors", "delete", 
        headers=get_api_headers(user), data={"color_ids": [color.id, 300]})
        new_color_count = Color.query.filter(Color.user_id == user.id).count()
        self.assertEqual(response.status_code , 404)
        self.assertEqual(new_color_count, old_color_count)


    def test_remove_colors(self): 
        color = Color.query.first() 
        user = User.query.get(color.user_id) 
        assert(user is not None)
        colors = Color.query.filter(Color.user_id == user.id).all()
        color_ids = list(map(lambda col: col.id, colors))
        old_color_count = len(colors)
        response = fetch(self.client, f"/api/v1/colors", "delete", 
        headers=get_api_headers(user), data={"color_ids": color_ids})
        new_color_count = Color.query.filter(Color.user_id == user.id).count()
        self.assertEqual(response.status_code , 200)
        self.assertEqual(new_color_count, 0)
