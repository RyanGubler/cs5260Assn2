import json
from requestFactory import RequestFactory
class RequestFactory:
    def create_request(self, database_type, request_type, request_data):
        if database_type == 's3':
            return RequestFactory.S3Request(request_type, request_data)
        elif database_type == 'dynamo':
            return RequestFactory.DynamoRequest(request_type, request_data)
        else:
            raise ValueError('Invalid database type')