import unittest
import os
import time
from unittest import TestCase
import ast
import sys
sys.path.append('../')
from app import server


dirname = os.path.dirname(__file__)
correct_file = os.path.join(dirname,'test_files/test.wig')
wrong_file = os.path.join(dirname,'test_files/test.txt')

class TestApp(TestCase):

    def setUp(self):
        self.app = server.app
        self.testing_client = self.app.test_client()

    def upload_file(self, file_path):
        with open(file_path, 'rb') as f:
            response = self.testing_client.post('/upload', data={'condition_1_forward_1': f})
            data = response.get_json()
        return response, data

    def test_upload_file(self):
        # Test successful file upload
        response, data = self.upload_file(correct_file)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Condition 1', data)
        self.assertIn('forward', data["Condition 1"])

        response = self.testing_client.get('/get_tss?jobid=' + data["Condition 1"]['forward'])
        while "Error" in response.get_json().keys():
            response = self.testing_client.get('/get_tss?jobid=' + data["Condition 1"]['forward'])

        # Test unsupported file format
        response, data = self.upload_file(wrong_file)
        self.assertEqual(response.status_code, 422)
        self.assertIn('Error', data)

    def test_get_wiggle_by_id(self):
        # Test getting file by valid id
        _, data = self.upload_file(correct_file)
        response = self.testing_client.get('/get_file?jobid='+data["Condition 1"]['forward'])
        self.assertEqual(response.status_code, 400)

        response = self.testing_client.get('/get_tss?jobid=' + data["Condition 1"]['forward'])
        while "Error" in response.get_json().keys():
            response = self.testing_client.get('/get_tss?jobid=' + data["Condition 1"]['forward'])

        response = self.testing_client.get('/get_file?jobid=' + data["Condition 1"]['forward'])
        self.assertEqual(response.status_code, 200)

        # Test getting file by invalid id
        response = self.testing_client.get('/get_file?jobid=invalid_id')
        self.assertEqual(response.status_code, 404)

    def test_get_job_state_by_id(self):
        # Test getting job state by valid id
        _, data = self.upload_file(correct_file)
        response = self.testing_client.get('/get_state?jobid='+data["Condition 1"]['forward'])
        self.assertEqual(response.status_code, 200)

        response = self.testing_client.get('/get_tss?jobid=' + data["Condition 1"]['forward'])
        while "Error" in response.get_json().keys():
            response = self.testing_client.get('/get_tss?jobid=' + data["Condition 1"]['forward'])

        # Test getting job state by invalid id
        response = self.testing_client.get('/get_state?jobid=invalid_id')
        self.assertEqual(response.status_code, 404)

    def test_get_tss_by_id(self):
        # Test getting TSS prediction by valid id
        _, data = self.upload_file(correct_file)
        response = self.testing_client.get('/get_tss?jobid='+data["Condition 1"]['forward'])
        self.assertEqual(response.status_code, 400)
        while "Error" in response.get_json().keys():
            response = self.testing_client.get('/get_tss?jobid=' + data["Condition 1"]['forward'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ast.literal_eval(response.data.decode('utf-8')), {"TSS Sites": []})

        # Test getting TSS prediction by invalid id
        response = self.testing_client.get('/get_tss?jobid=invalid_id')
        self.assertEqual(response.status_code, 404)

    def doCleanups(self):
        # cleanup any generated files
        for file in os.listdir(server.FILESTORE):
            os.remove(os.path.join(server.FILESTORE, file))


if __name__ == '__main__':
    unittest.main()
