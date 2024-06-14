from flask import Flask, request, render_template, url_for, redirect, Response, jsonify
from pymongo import MongoClient
import json
import random
import datetime
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.test_database
users = db.users
@app.route('/', methods=('GET', 'POST'))
def index():
    collections = list_collections()
    return render_template('index.html',datas = collections)


@app.route('/add', methods=('GET', 'POST'))
def add_post():
    if request.method == 'POST':
        category_name = request.form['category_name']
        name = request.form.get('name')
        degree = request.form.get('degree')
        db[category_name].insert_one(
            {
             'id':str(random.randint(1,9999)),
             'name':name,
             'degree':degree,
             'created_at': datetime.datetime.now()
             }
        )
    return redirect(url_for('index'))

"""
@app.route('/users', methods=['GET'])
def get_users():
    user_list = []
    all_users = users.find({})
    for user in all_users:
        user = {
            'id': user['id'],
            'name': user['name'],
            'degree': user['degree'],
            'created_at': user['created_at'],
        }
        user_list.append(user)
    return user_list
"""
@app.route('/delete', methods=('GET', 'POST'))
def delete_user():
    id = request.form.get('del_id')
    print(id,type(id))
    category_name = request.form.get('del_category')
    item = db[category_name].find_one({"id": id}) ## id'ye göre silmiyor anlamadım neden. İsim ve diğer şeyler için silebiliyor.
    print(item)
    db[category_name].delete_one(item)
    return redirect(url_for('index'))


@app.route('/update',methods=('GET', 'POST'))
def update_user():
    category_name = request.form.get('up_category')
    filterby = {"id": request.form.get('up_id')} ## aynı şekilde id'ye göre update etmiyor. İsim ve diğer şeyler için yapıyor
    new_values = {"$set":
        {
            'name': request.form.get('up_name'),
            'degree': request.form.get('up_degree'),
            'created_at': datetime.datetime.now()
        }

    }
    db[category_name].update_one(filterby, new_values)
    return redirect(url_for('index'))
"""
@app.route('/add_new_category',methods=('GET', 'POST'))
def new_category():
    category_name = request.form.get('cat_name')
    db[category_name]
    return  redirect(url_for('index'))
"""
@app.route('/update_category_name',methods=('GET', 'POST'))
def update_category_name():
    old_category_name = request.form.get('up_cat_name')
    new_category_name = request.form.get('new_cat_name')
    db[old_category_name].rename(new_category_name)
    return redirect(url_for('index'))

@app.route('/delete_category',methods=('GET', 'POST'))
def delete_category():
    filter = request.form.get('del_cat_name')
    if db[filter].find_one() == None:
        db[filter].drop()

    return redirect(url_for('index'))

@app.route('/list_collections', methods=('GET', 'POST'))
def list_collections():
    collectionItems = {}
    for collection in db.list_collection_names():
        collectionItems[collection] = db.get_collection(collection).find({})
    return json.loads(json_util.dumps(collectionItems))



if '__name__':
    app.run(debug=True)
