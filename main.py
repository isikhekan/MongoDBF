from flask import Flask, request, render_template, url_for, redirect, Response
from pymongo import MongoClient
import json

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/todo_db'
client = MongoClient('localhost', 27017)
db = client.todos


@app.route('/', methods=('GET', 'POST'))
def index():
    return 0
@app.route('/add',methods=['POST'])
def add_task():
    content = 'hkaan'
    degree = 'license'
    db_response = db.todo.insert_one({'content':content,'degree':degree})
    return Response(
        response = json.dumps({"message":'user created', 'id' : db_response.inserted_id}),
        status = 200,
        mimetype = 'application/json'
    )

if '__name__':
    app.run(debug=True)
