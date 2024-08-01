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
''''
    def test_addtask_returns_addedtask(self):
        with app.test_client() as client:
            import json
            response = client.post('/post/', data=json.dumps(
                    {
                        'id': 17,
                        'content': 'lalalla'
                    }
                ),
                content_type='application/json'
            )
            data = json.loads(response.data.decode('utf-8'))
            assert data['id'] == 17
            assert data['content'] == 'lalalla'
            assert data['status'] == False
'''
if __name__ == '__main__':
    unittest.main()
