from . import api 

@api.route("/tags")
def get_tags():
    pass 

@api.route("/tags", methods=["POST"])
def add_tag():
    pass 

@api.route("/tag/<tag_id>")
def get_tag_details():
    pass 

@api.route("/tag/<tag_id>", methods=["PUT"])
def get_edit_tag():
    pass 

@api.route("/tag/<tag_id>", methods=["DELETE"])
def remove_tag():
    pass 

@api.route("/tags", methods=["DELETE"])
def remove_tags():
    pass 

@api.route("/tag/<tag_id>")
def get_tag(tag_id):
    pass 

@api.route("/tag/<tag_id>/colors")
def get_colors_for_tag(tag_id):
    pass 