## Usage
Create a user
endpoint:/api/v1/users
method: POST
data-required:
	username: String,
	email: String,
	password: String

Get todo list:
endpoint:/api/v1/todos
method:GET

@login_required
Create a todo:
endpoint:/api/v1/todos
method: POST
data-required:
	name: String

@login_required
Update a todo:
endpoint:/api/v1/todos/<id>
method: PUT
data-required:
	name: String

@login_required
Delete a todo:
endpoint:/api/v1/todos/<id>
method: DELETE
