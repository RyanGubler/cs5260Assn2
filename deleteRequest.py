from request import Request
import boto3
import logging
import json

class DeleteRequest(Request):
    def __init__(self, request_type, request_data, database_type, consumer_bucket, sqs_url):
        logging.info(f"DeleteRequest: request_type={request_type}, request_data={request_data}")

        super().__init__(request_type, request_data)
        self.database_type = database_type
        self.consumer_bucket = consumer_bucket
        self.sqs_url = sqs_url
        
    def delete_sqs(self, message_receipt_handle):
        sqs = boto3.client('sqs', 'us-east-1')
        queue_url = self.sqs_url
        try:
            sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message_receipt_handle)
            logging.info(f'Message {message_receipt_handle} deleted from SQS')
        except Exception as e:
            logging.error(f'Error deleting message from SQS: {e}')

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
        print(f'Widget ID: {widget_id}')
        print(f'Owner: {owner}')
        if self.database_type == 's3':
            print("Deleting widget in S3")
            self.delete_s3(widget_id, owner)
        elif self.database_type == 'dynamo':
            print("Deleting widget in DynamoDB")
            self.delete_dynamo(widget_id)
        elif self.database_type == 'sqs':
            print("Deleting widget through SQS")
            self.delete_sqs(widget_id)
        else:
            raise ValueError(f'Invalid database type: {self.database_type}')