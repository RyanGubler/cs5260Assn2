import os
import json
import argparse
import logging
import jsonschema
import boto3
from requestFactory import RequestFactory

logging.basicConfig(filename='consumer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def argument_parser():
    parser = argparse.ArgumentParser(description='Process your widget requests with either S3 or DynamoDB.')
    parser.add_argument('--database-type', choices=['s3', 'dynamo'], required=True, help='Specify the type of the database (s3 or dynamoDB)')
    parser.add_argument('--producer-bucket', required=True, dest='producer_bucket', help='Specify the bucket that your producer is uploading to.')
    parser.add_argument('--consumer-bucket', required=True, dest='consumer_bucket', help='Specify the bucket that your consumer will upload to.')
    return parser.parse_args()

class Consumer:
    def __init__(self, schema_file, database_type, producer_bucket, consumer_bucket):
        self.s3 = boto3.client('s3')
        self.request_factory = RequestFactory()
        self.database_type = database_type
        self.producer_bucket = producer_bucket
        self.consumer_bucket = consumer_bucket
        with open(schema_file, 'r') as schema_file:
            self.widget_request_schema = json.load(schema_file)

    def get_s3_file_content(self, bucket_name, file_name):
        try:
            response = self.s3.get_object(Bucket=bucket_name, Key=file_name)
            file_content = response['Body'].read().decode('utf-8')
            widget_request_data = json.loads(file_content)
            return widget_request_data
        except Exception as e:
            logging.error(f'Error getting file content from S3: {e}')
            return None
        
    def validate_widget_request(self, widget_request_data):
        try:
            jsonschema.validate(widget_request_data, self.widget_request_schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            logging.error(e)
            return False

    def process_widget_requests(self):
        while True:
            try:
                response = self.s3.list_objects_v2(Bucket=self.producer_bucket)
                for obj in response.get('Contents', []):
                    file_name = obj['Key']
                    widget_request_data = self.get_s3_file_content(self.producer_bucket, file_name)
                    if self.validate_widget_request(widget_request_data):
                        request_instance = self.request_factory.create_request(self.database_type, widget_request_data['type'], widget_request_data)
                        request_instance.fill_attributes(widget_request_data)
                        request_instance.do_operation()
                        output_key = f'processed/{os.path.basename(file_name)}'
                        self.s3.put_object(Body=json.dumps(widget_request_data), Bucket=self.consumer_bucket, Key=output_key)
                        logging.info(f'Processed data uploaded to {output_key}')
            except Exception as e:
                logging.error(f'Error processing widget requests: {e}')


def main():
    args = argument_parser()
    database_type = args.database_type
    producer_bucket = args.producer_bucket
    consumer_bucket = args.consumer_bucket
    schema_file = 'widgetRequest-schema.json'
    consumer = Consumer(schema_file, database_type,producer_bucket, consumer_bucket)
    consumer.process_widget_requests()

if __name__ == '__main__':
    main()