import argparse
import time
import json
import boto3
import logging

logging.basicConfig(filename='consumer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
s3_client = boto3.client('s3')
dynamodb_client = boto3.client('dynamodb')

def clParser():
    parser = argparse.ArgumentParser(description='Consumer program for processing Widget Requests.')
    parser.add_argument('--storage-strategy', choices=['s3', 'dynamodb'], required=True)
    parser.add_argument('--bucket-name', help='S3 bucket name for Widget Requests')
    parser.add_argument('--dynamodb-table-name', help='DynamoDB table name for Widget Requests')
    args = parser.parse_args()
    return args

def get_widget_request(storage_strategy, bucket_name, dynamodb_table_name):
    if storage_strategy == 's3':
        try:
            response = s3_client.list_objects_v2(Bucket=bucket_name, MaxKeys=1)
            if 'Contents' in response:
                key = response['Contents'][0]['Key']
                obj = s3_client.get_object(Bucket=bucket_name, Key=key)
                widget_request = json.loads(obj['Body'].read().decode('utf-8'))
                s3_client.delete_object(Bucket=bucket_name, Key=key)
                return widget_request
        except Exception as e:
            logging.error(f'Error retrieving Widget Request from S3: {e}')
            return None
    elif storage_strategy == 'dynamodb':
        try:
            response = dynamodb_client.scan(TableName=dynamodb_table_name, Limit=1)
            items = response.get('Items', [])
            if items:
                widget_request = json.loads(items[0]['request_data']['S'])
                dynamodb_client.delete_item(TableName=dynamodb_table_name, Key={'request_id': items[0]['request_id']})
                return widget_request
        except Exception as e:
            logging.error(f'Error retrieving Widget Request from DynamoDB: {e}')
            return None
    return None

def process_widget_request(widget_request):
    pass

def main():
    args = clParser()
    storage_strategy = args.storage_strategy
    bucket_name = args.bucket_name
    dynamodb_table_name = args.dynamodb_table_name

    while True:
        widget_request = get_widget_request(storage_strategy, bucket_name, dynamodb_table_name)
        if widget_request:
            process_widget_request(widget_request)
        else:
            time.sleep(0.1)  # 100ms

if __name__ == '__main__':
    main()