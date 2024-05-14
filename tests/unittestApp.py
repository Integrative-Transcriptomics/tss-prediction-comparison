import unittest
import time
from unittest import TestCase
from app import server


class TestApp(TestCase):

    def setUp(self):
        self.app = server.app
        self.testing_client = self.app.test_client()

    def upload_file(self, file_path):
        with open(file_path, 'rb') as f:
            response = self.testing_client.post('/upload', data={'file': f})
            data = response.get_json()
            return response, data

    def test_upload_file(self):
        # Test successful file upload
        response, data = self.upload_file('test_files/test.wig')
        self.assertEqual(response.status_code, 200)
        self.assertIn('jobid', data)

        # Test unsupported file format
        response, data = self.upload_file('test_files/test.txt')
        self.assertEqual(response.status_code, 422)
        self.assertIn('Error', data)

    def test_get_wiggle_by_id(self):
        # Test getting file by invalid id
        response = self.testing_client.get('/get_file?jobid=invalid_id')
        self.assertEqual(response.status_code, 404)

    def test_get_job_state_by_id(self):
        # Test getting job state by valid id
        _, data = self.upload_file('test_files/test.wig')
        response = self.testing_client.get('/get_state?jobid='+data["jobid"])
        self.assertEqual(response.status_code, 200)

        # Test getting job state by invalid id
        response = self.testing_client.get('/get_state?jobid=invalid_id')
        self.assertEqual(response.status_code, 404)

    def test_get_tss_by_id(self):
        # Test getting TSS prediction by valid id
        _, data = self.upload_file('test_files/test.wig')
        response = self.testing_client.get('/get_tss?jobid='+data["jobid"])
        self.assertEqual(response.status_code, 400)

        # Test getting TSS prediction by invalid id
        response = self.testing_client.get('/get_tss?jobid=invalid_id')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
