from . import main 

@main.errorhandler(404)
def not_found():
    return "Not Found"