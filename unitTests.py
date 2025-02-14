import json
import unittest
from todoApp import app


class TestMethods(unittest.TestCase):
    def test_tasklist_return_status_200(self):
        with app.test_client() as client:
            response = client.get('/tasklist')
            assert response.status_code == 200

    def test_tasklist_must_have_json_format(self):
        with app.test_client() as client:
            response = client.get('/tasklist')
            assert response.content_type == 'application/json'

    def test_add_task_accepts_method_post(self):
        with app.test_client() as client:
            response = client.post('/post/')
            assert response.status_code != 405



if __name__ == '__main__':
    unittest.main()
