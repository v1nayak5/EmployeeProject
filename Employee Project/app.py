from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

import json

def load_employees_data():
    with open('data/employees.json', 'r') as file:
        data = json.load(file)
    return data['employees']


app = Flask(__name__)

# Database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_user'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'your_database'

mysql = MySQL(app)

# Create Employee Endpoint
@app.route('/api/create_employee', methods=['POST'])
def create_employee():
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    salary = data['salary']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO employees(first_name, last_name, salary) VALUES (%s, %s, %s)", (first_name, last_name, salary))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Employee created successfully'}), 201

# Get Employee by ID Endpoint
@app.route('/api/get_employee/<int:id>', methods=['GET'])
def get_employee(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employees WHERE id = %s", [id])
    employee = cur.fetchone()
    cur.close()
    if employee:
        return jsonify({'employee': employee}), 200
    else:
        return jsonify({'message': 'Employee not found'}), 404

# Query Employees Endpoint
@app.route('/api/query_employees', methods=['GET'])
def query_employees():
    name = request.args.get('name')
    from_salary = request.args.get('fromSalary')
    to_salary = request.args.get('toSalary')
    query_parts = ["SELECT * FROM employees WHERE"]
    query_params = []

    if name:
        query_parts.append("(first_name LIKE %s OR last_name LIKE %s)")
        query_params.extend([f"%{name}%", f"%{name}%"])

    if from_salary:
        query_parts.append("salary >= %s")
        query_params.append(from_salary)

    if to_salary:
        query_parts.append("salary <= %s")
        query_params.append(to_salary)

    # Removing initial condition if no parameters are provided
    if not (name or from_salary or to_salary):
        query_parts = ["SELECT * FROM employees"]

    query = " AND ".join(query_parts)
    cur = mysql.connection.cursor()
    cur.execute(query, query_params)
    employees = cur.fetchall()
    cur.close()
    return jsonify({'employees': employees}), 200

if __name__ == '__main__':
    app.run(debug=True)
