import unittest
from main import Consumer
from createRequest import CreateRequest
from requestFactory import RequestFactory
from createRequest import CreateRequest
from request import Request

class TestConsumer(unittest.TestCase):
    def test_schema(self):
        self.schema_file = 'widgetRequest-schema.json'

        self.consumer = Consumer(self.schema_file, 's3')
        self.consumer = Consumer(self.schema_file, 'dynamo')
    
    def test_storage_types(self):
        schema_file = 'widgetRequest-schema.json'
        input_bucket = 'usu-cs5260-goob-requests'
        output_bucket = 'usu-cs5260-goob-dist'
        storage_type_s3 = 's3'
        storage_type_dynamo = 'dynamo'
        consumer_s3 = Consumer(schema_file, storage_type_s3, input_bucket, output_bucket)
        self.assertEqual(consumer_s3.database_type, storage_type_s3)
        consumer_dynamo = Consumer(schema_file, storage_type_dynamo, input_bucket, output_bucket)
        self.assertEqual(consumer_dynamo.database_type, storage_type_dynamo)

class TestRequestFactory(unittest.TestCase):
    def test_factory(self):
        self.factory = RequestFactory()

    def test_create_request(self):
        self.factory = RequestFactory()
        request_type = 'create'
        database_type = 's3'
        request_data = {
            'type': 'create',
        }
        request_instance = self.factory.create_request(database_type, request_type, request_data)
        self.assertIsInstance(request_instance, CreateRequest)
        self.assertEqual(request_instance.database_type, database_type)

class TestRequest(unittest.TestCase):
    def test_constructor(self):
        request_type = 'create'
        request_data = {
            'requestId': '11111',
            'widgetId': '69420',
            'owner': 'Meeeeee',
            'label': 'Something',
            'description': 'Your mom',
            'otherAttributes': [
                {'name': 'not me', 'value': 'something not cool'},
                {'name': 'me', 'value': 'something cool'}
            ]
        }
        request_instance = Request(request_type, request_data)

        self.assertEqual(request_instance.type, request_type)
        self.assertEqual(request_instance.request_id, '11111')
        self.assertEqual(request_instance.widget_id, '69420')
        self.assertEqual(request_instance.owner, 'Meeeeee')
        self.assertEqual(request_instance.label, 'Something')
        self.assertEqual(request_instance.description, 'Your mom')
        self.assertEqual(request_instance.other_attributes, [
            {'name': 'not me', 'value': 'something not cool'},
            {'name': 'me', 'value': 'something cool'}
        ])

    def test_fill_attributes(self):
        request_instance = Request('', {})
        data = {
            'otherAttributes': [
                {'name': 'Your Mom', 'value': 'Old'},
                {'name': 'Me', 'value': 'Young'}
            ]
        }
        request_instance.fill_attributes(data)

        self.assertEqual(request_instance.other_attributes, [
            {'name': 'Your Mom', 'value': 'Old'},
            {'name': 'Me', 'value': 'Young'}
        ])

    def test_do_operation(self):
        request_instance = Request('', {})

if __name__ == '__main__':
    unittest.main()