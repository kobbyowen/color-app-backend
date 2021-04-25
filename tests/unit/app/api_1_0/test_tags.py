from app.models import User, Tag, Color
from app.database import db_session
from tests import DefaultTestCase 
from tests import fetch, get_api_headers, add_colors, add_tags
from app.errors import INSUFFICIENT_PERMISSION, VALIDATION_FAILED, \
    RESOURCE_NOT_FOUND, DUPLICATE_RESOURCE

class TagTestCase(DefaultTestCase):
    def setUp(self): 
        super().setUp()
        add_tags()
        add_colors()

    def tearDown(self):
        Tag.query.delete() 
        Color.query.delete() 
        db_session.commit() 
        db_session.commit() 
        super().tearDown()


class TestGetTagsEndpoint(TagTestCase):

    def test_get_tags(self): 
        response = fetch(self.client, "/api/v1/tags" ,
        headers=get_api_headers(User.query.first()))
        body = response.json
        self.assertEqual(len(body["tags"]), 3)
        self.assertEqual(response.status_code, 200)

    def test_get_individual_tag_that_dont_exist(self):
        response = fetch(self.client, "/api/v1/tag/20000", 
        headers=get_api_headers(User.query.first()))
        self.assertEqual(response.status_code, 404)

    def test_get_individual_tag_that_exist(self):
        tag = Tag.query.first() 
        response = fetch(self.client, f"/api/v1/tag/{tag.id}", 
        headers=get_api_headers(User.query.first()))
        self.assertEqual(response.status_code, 200)

    
    def test_get_tag_from_user_who_didnot_create_it(self):
        # the first user created all the tags, so get any other user 
        user = user = User.query.first()
        user = User.query.filter(User.id != user.id).first() 
        assert(user is not None)
        tag = Tag.query.first() 
        response = fetch(self.client, f"/api/v1/tag/{tag.id}", 
        headers=get_api_headers(user))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json["code"], INSUFFICIENT_PERMISSION)


class TestAddTagsEndpoint(TagTestCase):

    def test_add_tag_with_invalid_color_code(self): 
        for colorcode in ["kobby", "fffffff", "#ffffap", "#kobbyy"]:
            response = fetch(self.client, "/api/v1/tags", "post", 
            data={"color": colorcode, "name": "best"}, 
            headers=get_api_headers(User.query.first()))
            self.assertEqual(response.json["code"], VALIDATION_FAILED )

    def test_add_tag_with_name_that_already_exists(self): 
        name = Tag.query.first().name 
        response = fetch(self.client, "/api/v1/tags", "post", 
        data={"color": "#ddffff", "name": name}, 
        headers=get_api_headers(User.query.first()))
        self.assertEqual(response.json["code"], DUPLICATE_RESOURCE )

    def test_add_tag_with_long_name(self): 
        response = fetch(self.client, "/api/v1/tags", "post", 
        data={"color": "thisIsAVeryVeryLongNameToUseAsTagLabel", "name": "best"}, 
        headers=get_api_headers(User.query.first()))
        self.assertEqual(response.json["code"], VALIDATION_FAILED )

    def test_add_tag_with_invalid_name(self):
        for name in ["1kobby", "kobby-stone"]:
            response = fetch(self.client, "/api/v1/tags", "post", 
            data={"color": "#ffffff", "name": name}, 
            headers=get_api_headers(User.query.first()))
            self.assertEqual(response.json["code"], VALIDATION_FAILED )

    def test_add_valid_tag(self): 
        response = fetch(self.client, "/api/v1/tags", "post", 
        data={"color": "#ff0000", "name": "best"}, 
        headers=get_api_headers(User.query.first()))
        self.assertEqual(response.json["code"], 0 )
        self.assertEqual(response.status_code, 201)

class TestEditTagsEndpoint(TagTestCase):

    def test_edit_tag_with_invalid_name(self): 
        tag = Tag.query.first() 
        user = User.query.get(tag.user_id)

        response = fetch(self.client, f"/api/v1/tag/{tag.id}", "put", 
        data={"color": "#ff0000", "name": "best-2"}, 
        headers=get_api_headers(user))
        self.assertEqual(response.json["code"], VALIDATION_FAILED )

    def test_edit_tag_with_invalid_color(self): 
        tag = Tag.query.first() 
        user = User.query.get(tag.user_id)

        response = fetch(self.client, f"/api/v1/tag/{tag.id}", "put", 
        data={"color": "ff0000", "name": "best"}, 
        headers=get_api_headers(user))
        self.assertEqual(response.json["code"], VALIDATION_FAILED )
        
    def test_edit_tag_that_dont_exist(self): 
        tag = Tag.query.first() 
        user = User.query.get(tag.user_id)

        response = fetch(self.client, f"/api/v1/tag/400000000", "put", 
        data={"color": "#ff0000", "name": "best"}, 
        headers=get_api_headers(user))
        self.assertEqual(response.json["code"], RESOURCE_NOT_FOUND )
        
    def test_edit_tag_that_exist(self): 
        tag = Tag.query.first() 
        user = User.query.get(tag.user_id)
        response = fetch(self.client, f"/api/v1/tag/{tag.id}", "put", 
        data={"color": "#000000", "name": "replaced"}, 
        headers=get_api_headers(user))
        self.assertEqual(response.json["code"], 0 )
        tag = Tag.query.first()
        self.assertEqual(tag.name, "replaced")
        self.assertEqual(tag.color, "#000000")


class TestRemoveTagsEndpoint(TagTestCase):
    def test_remove_tag_with_nonexisting_id(self):
        tag = Tag.query.first() 
        user = User.query.get(tag.user_id)
        response = fetch(self.client, f"/api/v1/tag/400000000", "delete", 
        headers=get_api_headers(user))
        self.assertEqual(response.json["code"], RESOURCE_NOT_FOUND )

    def test_remove_list_of_tags_with_one_nonexisting_id(self):
        tag = Tag.query.first() 
        user = User.query.get(tag.user_id)
        id = tag.id 
        response = fetch(self.client, f"/api/v1/tags", "delete", 
        data={"tag_ids" : [id, 2000000]}, 
        headers=get_api_headers(user))
        self.assertEqual(response.json["code"], RESOURCE_NOT_FOUND )
        #check if first tag is not deleted
        self.assertIsNotNone(Tag.query.get(id)) 

    def test_remove_tag_that_exist(self):
        tag = Tag.query.first() 
        user = User.query.get(tag.user_id)
        response = fetch(self.client, f"/api/v1/tag/{tag.id}", "delete", 
        headers=get_api_headers(user))
        self.assertEqual(response.json["code"], 0 )

    def test_remove_list_of_tags_that_exist(self):
        tags = Tag.query.all() 
        user = User.query.get(tags[0].user_id)
        response = fetch(self.client, f"/api/v1/tags", "delete", 
        data={"tag_ids": [tag.id for tag in tags]},
        headers=get_api_headers(user))
        self.assertEqual(response.json["code"], 0 )

    def test_remove_list_of_tag_user_didnot_create(self):
        tag =Tag.query.first()
        user = User.query.get(tag.user_id )
        other_user = User.query.filter(User.id != user.id).first()
        # create tags for another user 
        tag1 = Tag(name = "mytag1", color="#ff0000", user_id=other_user.id)
        tag2 = Tag(name="mytag2", color="#00ff00", user_id=other_user.id)
        db_session.add_all([tag1, tag2])
        db_session.commit() 
        # send request
        response = fetch(self.client, f"/api/v1/tags", "delete", 
        data={"tag_ids": [tag1.id, tag.id ]},
        headers=get_api_headers(user))
        self.assertEqual(response.json["code"], INSUFFICIENT_PERMISSION )
        self.assertIsNotNone(Tag.query.get(tag1.id))
        self.assertIsNotNone(Tag.query.get(tag.id))



    