from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import configparser 

app = Flask(__name__)
app.config['DEBUG'] = True

# parse config ini file to get needed uri as described below
dbconfig = configparser.ConfigParser()
dbconfig.read("db-info.ini")
uristring = dbconfig.get("dbconfig","mysecret")

# type of database we are connecting to  '+' mysql driver then --> ://
# databaseuser:databasepassword@serveritliveson:portnumber/nameofthedatabasetoconnectto
app.config['SQLALCHEMY_DATABASE_URI']= uristring
# this setting allows for learning about ORM and how flask connects to database; 
# useful for debugging when database interactions are not as expected
# Will echo sql commands that are generated by sqlalchemy to the terminal
app.config['SQLALCHEMY_ECHO']=True

# calling sqlalchemy constructor with flask application as parameter
# will create database object that can be used within app to interface with DB via Python
db = SQLAlchemy(app)

# Create persistent class to represent app specific data to store in DB
# Class will represent tasks for our list

# specifies that class extends db.Model class; db is the object created from SQLAlchemy
# db object has a class inside of it called Model; 
# this will inherit basic functionality that allows "Task" objects to be translated to relation setting
class Task(db.Model):
    # data that is assc with id field of Task class will go into a DB column
    # within that constructor we define the field type and other info
    # column within table that represents Task -- datatype is integer, and primary key
    id=db.Column(db.Integer, primary_key=True)
    # column within table that represents Task -- datatype is string with max length 120 char
    name=db.Column(db.String(120))
    completed = db.Column(db.Boolean)

    # provide a contstructor for Task object -- take user specified and assign to column
    def __init__(self, name):
        self.name = name
        # Another option could be to set a default of false in the declaration
        self.completed = False

@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        task_name = request.form['task']
        # Create Task object with constructor
        new_task = Task(task_name)
        # Add new task object to db session
        db.session.add(new_task)
        # Push db session tasks to database
        db.session.commit()

    # populate variable with database entries
    tasks = Task.query.filter_by(completed=False).all()
    completed_tasks = Task.query.filter_by(completed=True).all()
    return render_template('todos.html',title="Get It Done!", tasks=tasks, completed_tasks=completed_tasks)

@app.route('/delete-task', methods=['POST'])
def delete_task():
    # Remove indicated task id from database
    task_id = int(request.form['task-id'])
    # query.get method calls a specific db entry by query
    task = Task.query.get(task_id)
    # delete the object returned from db query --> used task.id to grab object
    task.completed=True 
    db.session.add(task)
    db.session.commit()

    return redirect('/')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run()
