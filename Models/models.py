import json

from bson import ObjectId
from flask import Flask, request, render_template, url_for, redirect, Response, jsonify, Blueprint
from bson import json_util
import random
import datetime
from Database.database import create_db

collections = create_db()
categories = collections['categories']
books = collections['books']

simple_page = Blueprint('get-categories', __name__, template_folder='templates')


@simple_page.route('/categories/show_categories')
def show():
    print('abc2')
    return render_template('get-categories.html', data=json_util.dumps(categories.find()))


def show_categories():
    return render_template('categories.html')


@simple_page.route('/categories/update_category/<category_id>', methods=['GET', 'POST', 'PUT', 'PATCH'])
def update_category(category_id):
    filter = {'_id': ObjectId(category_id)}
    newCategoryName = request.form.get('name')
    print(newCategoryName, filter)
    categories.find_one_and_update(filter, {'$set': {"name": newCategoryName}})
    return redirect('http://127.0.0.1:5000/categories/show_categories')


@simple_page.route('/categories/delete_category/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    print(category_id, 'catid printed')
    if books.find_one({'category_id': ObjectId(category_id)}) == None:
        categories.delete_one({'_id': ObjectId(category_id)})
        print(categories.find(), 'deleted')

    return redirect('http://127.0.0.1:5000/categories/show_categories')


def add_book(title, creator, content, created_at, category_id):
    books.insert_one(
        {
            'title': title,
            'creator': creator,
            'content': content,
            'created_at': created_at,
            'category_id': category_id
        }
    )


def get_books():
    return books.find()
