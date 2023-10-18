import json
from createRequest import CreateRequest
class RequestFactory:
    def create_request(self, database_type, request_type, request_data):
        if database_type == 's3':
            return CreateRequest(request_type, request_data)
        elif database_type == 'dynamo':
            return CreateRequest(request_type, request_data)
        else:
            raise ValueError('Invalid database type')
    