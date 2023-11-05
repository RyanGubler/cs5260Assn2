from createRequest import CreateRequest
from updateRequest import UpdateRequest
from deleteRequest import DeleteRequest
class RequestFactory:
    def create_request(self, database_type, request_type, request_data, consumer_bucket, sqs_url):
        if request_type == 'create':
            return CreateRequest(request_type, request_data, database_type, consumer_bucket, sqs_url)
        elif request_type == 'update':
            print('went to update')
            return UpdateRequest(request_type, request_data, database_type, consumer_bucket, sqs_url)
        elif request_type == 'delete':
            print('went to delete')
            return DeleteRequest(request_type, request_data, database_type, consumer_bucket, sqs_url)
        else:
            raise ValueError('Invalid request type')