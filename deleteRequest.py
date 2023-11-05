from request import Request
import boto3
import logging
import json

class DeleteRequest(Request):
    def __init__(self, request_type, request_data, database_type, consumer_bucket):
        super().__init__(request_type, request_data)
        self.database_type = database_type
        self.consumer_bucket = consumer_bucket
        
    def delete_s3(self, widget_id, owner):
        s3 = boto3.client('s3')
        bucket_name = self.consumer_bucket
        object_key = f'widgets/{owner}/{widget_id}'
        s3.delete_object(Bucket=bucket_name, Key=object_key)
        logging.info(f'Widget {widget_id} deleted from S3.')

    def delete_dynamo(self, widget_id):
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table_name = 'widgets'
        table = dynamodb.Table(table_name)
        response = table.delete_item(Key={'id': widget_id})
        logging.info(f'Widget {widget_id} deleted from DynamoDB.')

    def do_operation(self):
        widget_id = self.request_data['widget_id']
        owner = self.request_data['owner']
        if self.database_type == 's3':
            self.delete_s3(widget_id, owner)
        elif self.database_type == 'dynamo':
            self.delete_dynamo(widget_id)
        else:
            raise ValueError('Invalid database type')