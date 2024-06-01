from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employeeworktime.db'

db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    worktime = db.Column(db.String(50))

    def __init__(self, name, worktime):
        self.name = name
        self.worktime = worktime

with app.app_context():
    db.create_all()

@app.route('/add_employee', methods=['POST'])
def add_employee():
    name = request.form['name']
    worktime = request.form['worktime']
    employee = Employee(name, worktime)
    db.session.add(employee)
    db.session.commit()
    return {"message": "Employee added successfully"}

@app.route('/get_employee/<int:id>')
def get_employee(id):
    employee = Employee.query.get(id)
    if employee:
        return jsonify({
            'id': employee.id,
            'name': employee.name,
            'worktime': employee.worktime
        })
    else:
        return {'error': 'Employee not found'}, 404

@app.route('/delete_employee/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get(id)
    if employee:
        db.session.delete(employee)
        db.session.commit()
        return {'message': 'Employee deleted successfully'}
    else:
        return {'error': 'Employee not found'}, 404

@app.route('/get_all_employee', methods=['GET'])
def get_all_employee():
    employee = Employee.query.all()
    result = []
    for employee in employee:
        result.append({
            'id': employee.id,
            'name': employee.name,
            'worktime': employee.worktime
        })
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

#import requests as r
#res = r.post(url = "http://127.0.0.1:5000/add_employee", data = {'name': '', "worktime": ""})
#res = r.get(url = "http://127.0.0.1:5000/get_employee/")
#res = r.delete(url = "http://127.0.0.1:5000/delete_employee/")
#r.get(url = "http://127.0.0.1:5000/get_all_employee")