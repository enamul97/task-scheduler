import mysql.connector
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)


db_config = {
    'host': 'localhost',
    'user': 'root',            
    'password': 'root',        
    'database': 'tasks_management_db'     
}


def get_db_connection():
    return mysql.connector.connect(**db_config)


@app.route('/tasks', methods=['GET'])
def get_tasks():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)  
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify({"tasks": tasks})


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task = cursor.fetchone()
    cursor.close()
    connection.close()
    if task:
        return jsonify(task)
    else:
        return jsonify({"message": "Task not found"}), 404


@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json or 'status' not in request.json:
        return jsonify({"message": "Bad request, 'title' and 'status' are required"}), 400

    title = request.json['title']
    description = request.json.get('description', '')
    status = request.json['status']
    due_date = request.json.get('due_date', None)

 
    if due_date:
        try:
            due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"message": "Invalid date format. Use YYYY-MM-DD"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, description, status, due_date) VALUES (%s, %s, %s, %s)",
        (title, description, status, due_date)
    )
    connection.commit()
    task_id = cursor.lastrowid  
    cursor.close()
    connection.close()
    return jsonify({"id": task_id, "title": title, "description": description, "status": status, "due_date": due_date}), 201


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = request.json
    title = task.get('title')
    description = task.get('description')
    status = task.get('status')
    due_date = task.get('due_date')

    if due_date:
        try:
            due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"message": "Invalid date format. Use YYYY-MM-DD"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE tasks SET title = %s, description = %s, status = %s, due_date = %s WHERE id = %s",
        (title, description, status, due_date, task_id)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"id": task_id, "title": title, "description": description, "status": status, "due_date": due_date})


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "Task deleted successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)
