from flask import jsonify, request
class BaseService:
    def handle_request(self, request_body, controller_method):
        result, error = controller_method(request_body) if request_body else controller_method()
        response = result if not error else {'error': error}
        status_code = 200 if result else 404 if not error else 400
        return jsonify(response), status_code

    def create(self, controller_method):
        return self.handle_request(request.json, controller_method)
    
    def update(self, controller_method):
        return self.handle_request(request.json, controller_method)
    
    def get_by_id(self, _id, controller_method):
        return self.handle_request(_id, controller_method)
    
    def get_all(self, controller_method):
        return self.handle_request(None, controller_method)
