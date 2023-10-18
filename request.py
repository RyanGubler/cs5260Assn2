import json
import logging

class Request:
    def __init__(self, request_type, request_data):
        self.type = request_type
        self.request_id = request_data.get('requestId', '')
        self.widget_id = request_data.get('widgetId', '')
        self.owner = request_data.get('owner', '')
        self.label = request_data.get('label', '')
        self.description = request_data.get('description', '')
        self.other_attributes = request_data.get('otherAttributes', [])

    def fill_attributes(self, data):
        if 'otherAttributes' in data:
            self.other_attributes = []
            for attribute in data['otherAttributes']:
                if 'name' in attribute and 'value' in attribute:
                    parsed_attribute = {
                        'name': attribute['name'],
                        'value': attribute['value']
                    }
                    self.other_attributes.append(parsed_attribute)
                else:
                    logging.warning("There was an issue with the otherAttribute format in the request")
        else:
            logging.warning("otherAttributes key is missing. So sorry!")

    def do_operation(self):
        pass #abstract method