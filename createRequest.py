from request import Request


class CreateRequest(Request):
    def __init__(self, request_type, request_data):
        super().__init__(request_type, request_data)

    def fill_attributes(self, data):
        # Parse JSON data specific to create request
        # Additional logic for parsing create request attributes
        pass

    def do_operation(self):
        # Implement logic for handling create operation
        # For example, code to create a widget in the specified storage mechanism
        print(f'Creating widget: {self.widget_id} for owner: {self.owner}')

# Example usage of CreateRequest
request_data = {
    'requestId': '123',
    'widgetId': '456',
    'owner': 'Alice',
    'label': 'Sample Widget',
    'description': 'This is a test widget.'
}

create_request = CreateRequest('create', request_data)
create_request.fill_attributes(request_data)
create_request.do_operation()