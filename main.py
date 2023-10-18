import os
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
    sample_requests = 'sample-requests/'

    if not os.path.exists(sample_requests):
        logging.error(f'Request folder not found: {sample_requests}')
        return
    request_factory = RequestFactory()
    database_type = input("Which database do you want to use? (s3 or dynamo): ")
    if database_type != 's3' or database_type != 'dynamo':
        print("Thats not a valid database option")
        return
    for file in os.listdir(sample_requests):
        file_path = os.path.join(sample_requests, file)
        with open(file_path, 'r') as file_name:
            try:
                widget_request_data = json.load(file_name)
            except json.JSONDecodeError as e:
                logging.error(f'Error decoding JSON in file {file}')
                continue

            if validate_widget_request(widget_request_data):
                request_instance = request_factory.create_request(database_type, widget_request_data['type'], widget_request_data)
                request_instance.fill_attributes(widget_request_data)
                request_instance.do_operation()

if __name__ == '__main__':
    main()