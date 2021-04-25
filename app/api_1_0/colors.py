from . import api 

@api.route("/colors")
def get_colors(): pass

@api.route("/colors/<color_id>")
def get_color(color_id):
    pass 


@api.route("/colors/unrated")
def get_unrated_colors(): pass 


@api.route("/colors/starred")
def get_starred_colors(): pass 

@api.route("/colors/liked")
def get_liked_colors(): pass 

@api.route("/colors/loved")
def get_loved_colors(): pass 

@api.route("/colors/favorite")
def get_fav_colors(): pass

@api.route("/colors/vic")
def get_vic_colors():
    pass

@api.route("/colors", methods=["POST"])
def add_color():
    pass 

@api.route("/colors/<color_id>", methods=["PUT"])
def edit_colors(color_id):
    pass 

@api.route("/colors/<color_id>", methods=["DELETE"])
def remove_color(color_id):
    pass

@api.route("/colors", methods=["DELETE"])
def remove_colors():
    pass 


