from request import Request
import boto3
import logging
import json

class UpdateRequest(Request):
    def __init__(self, request_type, request_data, database_type, consumer_bucket):
        super().__init__(request_type, request_data)
        self.database_type = database_type
        self.consumer_bucket = consumer_bucket
    def update_s3(self, data):
        s3 = boto3.client
        bucket_name = self.consumer_bucket
        object_key = f'widgets/{data["owner"]}/{data["widget_id"]}'
        s3.put_object(Body=json.dumps(data), Bucket=bucket_name, Key=object_key)
        logging.info(f'Widget {data["widget_id"]} updated in S3.')

    def update_dynamo(self, widget_data):
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table_name = 'widgets'
        table = dynamodb.Table(table_name)

        widget_item = {
            'id': widget_data['widget_id'],
            'request_id': widget_data['request_id'],
            'owner': widget_data['owner'],
            'label': widget_data['label'],
            'description': widget_data['description'],
            'other_attributes': widget_data['other_attributes']
        }
        table.put_item(Item=widget_item)
        logging.info(f'Widget {widget_data["widget_id"]} updated in DynamoDB.')

    def do_operation(self):
        if self.database_type == 's3':
            self.update_s3(self.request_data)
        elif self.database_type == 'dynamo':
            self.update_dynamo(self.request_data)
        else:
            raise ValueError("Invalid database type")