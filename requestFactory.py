from createRequest import CreateRequest
from updateRequest import UpdateRequest
from deleteRequest import DeleteRequest
class RequestFactory:
    def create_request(self, database_type, request_type, request_data):
        if request_type == 'create':
            return CreateRequest(request_type, request_data, database_type)
        elif request_type == 'update':
            return UpdateRequest(request_type, request_data, database_type)
        elif request_type == 'delete':
            return DeleteRequest(request_type, request_data, database_type)
        else:
            raise ValueError('Invalid request type')