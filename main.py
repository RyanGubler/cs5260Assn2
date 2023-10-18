import json
import logging
import jsonschema
from requestFactory import RequestFactory

logging.basicConfig(filename='consumer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

with open('widgetRequest-schema.json', 'r') as schema_file:
    widget_request_schema = json.load(schema_file)

def validate_widget_request(widget_request_data):
    try:
        jsonschema.validate(widget_request_data, widget_request_schema)
        return True
    except jsonschema.exceptions.ValidationError as e:
        logging.error(f'Invalid Widget Request: {e}')
        return False

def main():
    pass

if __name__ == '__main__':
    main()