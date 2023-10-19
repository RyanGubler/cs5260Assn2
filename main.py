import os
import json
import logging
import jsonschema
from requestFactory import RequestFactory

logging.basicConfig(filename='consumer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Consumer:
    def __init__(self, schema_file):
        self.sample_requests = 'sample-requests/'
        self.request_factory = RequestFactory()
        with open(schema_file, 'r') as schema_file:
            self.widget_request_schema = json.load(schema_file)

    def validate_widget_request(self, widget_request_data):
        try:
            jsonschema.validate(widget_request_data, self.widget_request_schema)
            logging.info('Widget Request Successful')
            return True
        except jsonschema.exceptions.ValidationError as e:
            logging.error(f'Widget Request Failure: {e}')
            return False

    def process_widget_requests(self, database_type):
        for file in os.listdir(self.sample_requests):
            file_path = os.path.join(self.sample_requests, file)
            with open(file_path, 'r') as file_name:
                try:
                    widget_request_data = json.load(file_name)
                except json.JSONDecodeError as e:
                    logging.error(f'Error decoding JSON in file {file}')
                    continue
                if self.validate_widget_request(widget_request_data):
                    request_instance = self.request_factory.create_request(database_type, widget_request_data['type'], widget_request_data)
                    request_instance.fill_attributes(widget_request_data)
                    request_instance.do_operation()

def main():
    schema_file = 'widgetRequest-schema.json'
    consumer = Consumer(schema_file)
    database_type = input("Which storage system do you want to use? (s3 or dynamo) I am assuming you will use good input: ")
    consumer.process_widget_requests(database_type)

if __name__ == '__main__':
    main()