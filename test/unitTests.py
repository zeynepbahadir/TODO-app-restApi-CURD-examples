import unittest
import sys
import os

## Add the parent directory to Python path to find the source package
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Add both source and test directories to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
sys.path.append(os.path.join(parent_dir, 'source'))

from source.todoApp import app
from source.sqlOperations import SqlOperation
from http import HTTPStatus

class TestClass_00_TodoApp(unittest.TestCase):
    """Test cases for Todo application API endpoints."""
    
    def setUp(self):
        """Set up test client and other test variables."""
        self.sql_op = SqlOperation("todoDB.db")

        self.app = app.test_client()
        self.app.testing = True

        # Test data
        self.sample_task = {
            'content': 'Test task',
            'status': False
        }
        
        self.invalid_task = {
            'NOcontent': 'Missing ID'
        }

    def test_00_tasklist_must_have_statuscode_ok(self):
        """Test that response status code is OK."""
        response = self.app.get('/api/tasks')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_01_tasklist_must_have_json_format(self):
        """Test that response content type is application/json."""
        response = self.app.get('/api/tasks')
        self.assertEqual(response.content_type, 'application/json')

    def test_02_create_task_success(self):
        """Test successful task creation."""
        response = self.app.post('/api/tasks', json=self.sample_task)
        id = self.sql_op.fetch_last_id()
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertIn('message', response.json)
        self.app.delete(f'/api/tasks/{id}')

    def test_03_create_task_missing_fields(self):
        """Test task creation with missing required fields."""
        response = self.app.post('/api/tasks', json=self.invalid_task)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn('error', response.json)

    def test_04_create_task_no_data(self):
        """Test task creation with no data."""
        response = self.app.post('/api/tasks')
        self.assertEqual(response.status_code, HTTPStatus.INTERNAL_SERVER_ERROR)

    def test_05_get_task_statuscode_ok(self):
        """Test successful task retrieval."""        
        # Get task
        id = self.sql_op.fetch_last_id()
        response = self.app.get(f'/api/tasks/{id}')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        
    def test_06_get_task_success(self):
        """Test successful task retrieval."""
        id = self.sql_op.fetch_last_id()
        response = self.app.get(f'/api/tasks/{id}')
        task_data = response.json
        self.assertEqual(task_data[1], self.sample_task['content'])

    def test_07_get_task_not_found(self):
        """Test getting non-existent task."""
        response = self.app.get('/api/tasks/999')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertIn('error', response.json)

    def test_08_update_task_statuscode_ok(self):
        """Test successful task status update."""
        self.app.post('/api/tasks', json=self.sample_task)
        # Update task
        id = self.sql_op.fetch_last_id()
        response = self.app.put(f'/api/tasks/{id}')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.app.delete(f'/api/tasks/{id}')
        
    def test_09_update_task_success(self):
        """Test successful task status update."""
        self.app.post('/api/tasks', json=self.sample_task)
        # Verify status changed
        id = self.sql_op.fetch_last_id()
        self.app.put(f'/api/tasks/{id}')
        get_response = self.app.get(f'/api/tasks/{id}')
        self.assertTrue(get_response.json[2])  # Check if status is True
        self.app.delete(f'/api/tasks/{id}')

    def test_10_update_task_not_found(self):
        """Test updating non-existent task."""
        response = self.app.put('/api/tasks/999')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_11_delete_task_statuscode_ok(self):
        """Test successful task deletion status code."""
        self.app.post('/api/tasks', json=self.sample_task)
        id = self.sql_op.fetch_last_id()
        # Delete task
        response = self.app.delete(f'/api/tasks/{id}')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        
    def test_12_delete_task_success(self):
        """Test successful task deletion."""
        self.app.post('/api/tasks', json=self.sample_task)
        id = self.sql_op.fetch_last_id()
        self.app.delete(f'/api/tasks/{id}')
        # Verify task was deleted
        response = self.app.get(f'/api/tasks/{id}')
        self.assertIn('error', response.json)

    def test_13_delete_task_not_found(self):
        """Test deleting non-existent task."""
        response = self.app.delete('/api/tasks/999')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_14_404_handler(self):
        """Test 404 error handler."""
        response = self.app.get('/nonexistent/endpoint')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertIn('error', response.json)

    def tearDown(self):
        """Clean up after each test."""
        # Delete all tasks from test database
        #try:
        #    tasks = self.sql_op.select_all_tasks()
        #    for task in tasks:
        #        self.sql_op.delete_task(task[0])
        #except Exception:
        pass


class TestClass_01_SQLOP(unittest.TestCase):
    """Test cases for SQL Operations."""

    def setUp(self):
        # Initialize test database
        self.sql_op = SqlOperation("test/test_todoDB.db")
        self.sql_op.create_table()
        
        # Test data
        self.sample_task = {
            'content': 'Test task',
            'status': False
        }
        
        self.invalid_task = {
            'content': 'Missing ID'
        }
    
    def test_00_get_empty_tasklist_from_DB(self):
        """Test for empty database."""
        x = self.sql_op.select_all_tasks()
        self.assertListEqual(x, [])

    def test_01_create_task(self):
        """Test for add task."""
        task = self.sample_task['content']
        self.sql_op.add_task(task)
        self.assertEqual((1, "Test task", False), self.sql_op.get_task("1"))
    
    def test_02_get_task(self):
        """Test for get the task."""
        self.assertEqual((1, "Test task", False), self.sql_op.get_task("1"))   
    
    def test_03_update_task(self):
        """Test for update the task."""
        self.sql_op.update_task("1")
        self.assertEqual((1, "Test task", True), self.sql_op.get_task("1"))
        self.sql_op.update_task("1")
        self.assertEqual((1, "Test task", False), self.sql_op.get_task("1"))

    def test_04_delete_task(self):
        """Test for delete the task."""
        self.sql_op.delete_task("1")
        self.assertIsNone(self.sql_op.get_task("1"))

    def test_05_generate_unique_id(self):
        task = self.sample_task['content']
        for id in range(1, 15):
            self.sql_op.add_task(task)
            self.assertEqual((id, "Test task", False), self.sql_op.get_task(f"{id}"))
       
    @classmethod
    def tearDownClass(cls) -> None:
        os.remove("test/test_todoDB.db")

if __name__ == '__main__':
    unittest.main()
