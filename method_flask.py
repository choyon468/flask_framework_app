from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# config the connection string
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///demo.db'


# to use mysql need to install pymysql

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# intializing alchemy
db = SQLAlchemy(app)
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable = False)
    lastname = db.Column(db.String, nullable = False)
    age = db.Column(db.Integer, nullable = False)
    salary = db.Column(db.Integer, nullable = False)

    def to_dict(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'age': self.age,
            'salary': self.salary,
          # Include other fields as necessary
       }
    
with app.app_context():
    db.create_all()


@app.route('/flaskemployees/', methods=['GET'])
def get_employees():
    employees = Employee.query.all()
    return jsonify([employee.to_dict() for employee in employees])

@app.route('/flaskemployees/<int:id>',methods=['GET'])
def get_employee(id):
    employee = Employee.query.get(id)
    if employee is None:
        return  jsonify({"error":"No Employee found!"})
    return jsonify(employee.to_dict())

@app.route('/flaskemployees/', methods = ['POST'])
def create_employee():
    data = request.json
    employee = Employee(firstname=data['firstname'], lastname=data['lastname'], age=data['age'], salary=data['salary'])
    db.session.add(employee)
    db.session.commit()
    return jsonify(employee.to_dict()), 201

@app.route('/flaskemployees/<int:id>', methods=['PUT'])
def update_employee(id):
    employee = Employee.query.get(id)
    if employee is None:
        return jsonify({"error": "No Employee found!"})
    data = request.json
    employee.firstname = data['firstname']
    employee.lastname = data['lastname']
    employee.age = data['age']
    employee.salary = data['salary']
    db.session.commit()
    return jsonify(employee.to_dict())


@app.route('/flaskemployees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    employee = Employee.query.get(id)
    if employee is None:
        return jsonify({"error": "No Employee found!"})
    db.session.delete(employee)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"})



if __name__ == '__main__':
    app.run(debug=True)