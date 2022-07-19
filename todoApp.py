from flask import Flask, jsonify, request, redirect, url_for
import json
import sqlOperations

sqlOp = sqlOperations.SqlOperation()
sqlOp.create_table()


app = Flask('todoapp')


@app.route('/tasklist')
def listing():
    if request.method == 'GET':
        mytb = sqlOp.select_all_tasks()
        return jsonify(json.dumps(mytb))


@app.route('/post/', methods=['POST'])
def post():
    if request.method == 'POST':
        myid = request.args['id']
        mycontent = request.args['content']
        task = (myid, mycontent, False)
        sqlOp.add_task(task)
        sqlOp.select_all_tasks()
        return jsonify('posted')

@app.route('/tasks/<id_>', methods=['GET'])
def get(id_):
    if request.method == 'GET':
        return jsonify(json.dumps(sqlOp.get_task(id_)))


@app.route('/tasks/<id_>', methods=['PUT'])
def update(id_):
    if request.method == 'PUT':
        sqlOp.update_task(id_)
        return jsonify("changed status of the task ", id_)


@app.route('/tasks/<id_>', methods=['DELETE'])
def delete(id_):
    if request.method == 'DELETE':
        sqlOp.delete_task(id_)
        return jsonify("deleted the task ", id_)


if __name__ == '__main__':
    app.run()
