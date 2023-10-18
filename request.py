import json

class Request:
    def __init__(self, request_type, request_data):
        self.type = request_type
        self.request_id = request_data.get('requestId', '')
        self.widget_id = request_data.get('widgetId', '')
        self.owner = request_data.get('owner', '')
        self.label = request_data.get('label', '')
        self.description = request_data.get('description', '')
        self.other_attributes = request_data.get('otherAttributes', '')

    def fill_attributes(self, data):
        # Implement JSON parsing logic specific to the request data structure
        pass

    def do_operation(self):
        # Abstract method, to be implemented by child classes
        pass