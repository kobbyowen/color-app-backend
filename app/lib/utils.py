from flask import jsonify 

class Rest:
    SUCCESS = 0 
    ERROR = 1

    @classmethod
    def return_response( cls, code: int, message:str, data: dict, 
                        response_code:int, headers:dict):
        response = { "errorCode" : code , "message": message }
        response.update( data )
        return jsonify(response), response_code, headers 
    
    @classmethod
    def success(cls, code:int=0, message:str="Successful", data={}, 
                    response_code=200, **headers):
        return cls.return_response(code, message, data, response_code, headers )

    @classmethod
    def error( cls, code: int=1, message:str="An error occurred", data={},
            response_code=400, **headers):
             return cls.return_response(code, message, data, response_code, headers )