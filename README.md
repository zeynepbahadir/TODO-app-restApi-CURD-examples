# TODO-app-restApi-CRUD-examples

A Flask-based REST API application demonstrating CRUD (Create, Read, Update, Delete) operations for a TODO list manager.

## Features

- RESTful API endpoints
- SQLite database integration
- Automatic unique ID generation
- JSON response format
- Comprehensive error handling
- Unit tests

## Project Structure

- `source/todoApp.py`: Main application file
- `source/sqlOperations.py`: Database operations
- `test/unitTests.py`: Unit tests
- `requirements.txt`: Dependencies
- `README.md`: This file

## Installation

1. Clone the repository:


bash
git clone https://github.com/yourusername/todo-app-restapi-crud.git
cd todo-app-restapi-crud


2. Install dependencies:

bash
pip install -r requirements.txt


3. Run the application:

bash
python source/todoApp.py


## API Endpoints

### Get All Tasks

bash
GET /api/tasks

### Create a New Task

bash
POST /api/tasks


### Get a Task by ID

bash
GET /api/tasks/<task_id>


### Update a Task

bash
PUT /api/tasks/<task_id>


### Delete a Task

bash
DELETE /api/tasks/<task_id>


## Error Handling

### 404 Not Found

bash
GET /api/tasks/nonexistent


### 500 Internal Server Error

bash
POST /api/tasks


## Unit Tests

bash
python -m unittest test/unitTests.py


## Key Implementations Details

### Database Operations

### todoApp.py
- Flask application
- SQLite database connection
- CRUD operations
- Error handling
- Unit tests

### sqlOperations.py
- Database connection
- CRUD operations
- Error handling
- Unit tests

### unitTests.py
- Comprehensive test coverage
- Database operation testing
- API endpoint testing
- Error case validation


## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes and commit them
4. Push to the branch
5. Create a pull request


## License

This project is licensed under the MIT License. See the LICENSE file for details.


## Contact

For questions or feedback, please contact [zeynep1bahadir@gmail.com](zeynep1bahadir@gmail.com).