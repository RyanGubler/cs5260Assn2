from request import Request
import boto3
import logging
import json

class CreateRequest(Request):
    def __init__(self, request_type, request_data, database_type):
        super().__init__(request_type, request_data)
        self.database_type = database_type
    def create_s3(self):
        s3 = boto3.client('s3')
        bucket_name = 'usu-cs-5260-goob-requests'
        widget_data = {
            'request_id': self.request_id,
            'widget_id': self.widget_id,
            'owner': self.owner,
            'label': self.label,
            'description': self.description,
            'other_attributes': self.other_attributes
        }
        try:
            s3.put_object(Bucket=bucket_name, Key=f'widgets/{self.owner}/{self.widget_id}.json', Body=json.dumps(widget_data))
            logging.info(f'Widget {self.widget_id} created in S3')
        except Exception as e:
            logging.error(f'Error creating widget in S3: {e}')

    def create_dynamo(self):
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table_name = 'widgets'
        table = dynamodb.Table(table_name)

        widget_item = {
            'request_id': self.request_id,
            'widget_id': self.widget_id,
            'owner': self.owner,
            'label': self.label,
            'description': self.description,
            'other_attributes': self.other_attributes
        }

        try:
            table.put_item(Item=widget_item)
            logging.info(f'Widget {self.widget_id} created in DynamoDB.')
        except Exception as e:
            logging.error(f'Error creating widget in DynamoDB: {e}')

    def do_operation(self):
        if self.database_type == 's3':
            print("creating widget in S3")
            self.create_s3()
        elif self.database_type == 'dynamo':
            print("Creating widget in DynamoDB")
            self.create_dynamo()
        else:
            raise ValueError('Invalid database type')

