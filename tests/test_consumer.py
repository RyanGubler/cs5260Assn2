import unittest
from unittest.mock import patch
from main import get_widget_request

class TestConsumer(unittest.TestCase):

    @patch('consumer.s3_client.list_objects_v2')
    @patch('consumer.s3_client.get_object')
    @patch('consumer.s3_client.delete_object')
    def test_get_widget_request_from_s3(self, mock_delete_object, mock_get_object, mock_list_objects_v2):
        mock_list_objects_v2.return_value = {'Contents': [{'Key': 'widgets/test-owner/test-id'}]}
        mock_get_object.return_value = {'Body': {'obj_key': 'obj_value'}}

        result = get_widget_request('s3', 'test-bucket', 'test-table')

        self.assertEqual(result, {'obj_key': 'obj_value'})
        mock_list_objects_v2.assert_called_once_with(Bucket='test-bucket', MaxKeys=1)
        mock_get_object.assert_called_once_with(Bucket='test-bucket', Key='widgets/test-owner/test-id')
        mock_delete_object.assert_called_once_with(Bucket='test-bucket', Key='widgets/test-owner/test-id')

if __name__ == '__main__':
    unittest.main()