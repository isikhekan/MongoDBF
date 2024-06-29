from bson import ObjectId
from flask import Flask, render_template, url_for, redirect, Response, jsonify
from bson import json_util
import random
import datetime
from Database.database import create_db
from Models.models import add_book, get_books

pages = {
    'show_all_category_page': 'http://127.0.0.1:5000/categories/show_all'
}
collections = create_db()
books = collections['books']
categories = collections['categories']


def db_add_book(request):
    title = request.form.get('title')
    creator = request.form.get('creator')
    content = request.form.get('content')
    created_at = datetime.datetime.now()
    if request.form.get('createnadd'):
        if categories.find_one({'name': request.form.get('category_name')}) == None:
            categories.insert_one({'name': request.form.get('category_name')})
        category = categories.find_one({'name': request.form.get('category_name')})
        category_id = category['_id']
        add_book(title, creator, content, created_at, category_id)
        return render_template('index.html',
                               data={'all_books': json_util.dumps(get_books()), 'error': '', 'success': True})
    else:
        if categories.find_one({'name': request.form.get('category_name')}) != None:
            category_id = categories.find_one({'name': request.form.get('category_name')})['_id']
            add_book(title, creator, content, created_at, category_id)
            return render_template('index.html',
                                   data={'all_books': json_util.dumps(get_books()), 'error': '', 'success': True})
        return render_template('index.html', data={'all_books': json_util.dumps(get_books()),
                                                   'error': 'You must add category before adding book to not exist category',
                                                   'success': False})


def db_del_book(book_id):
    books.delete_one({'_id': ObjectId(book_id)})


def db_update_book(book_id, request):
    filter = {"_id": ObjectId(book_id)}
    new_values = {"$set":
        {
            'title': request.form.get('title'),
            'creator': request.form.get('creator'),
            'content': request.form.get('content'),
            'created_at': datetime.datetime.now()
        }}
    print(new_values)
    books.find_one_and_update(filter, new_values)
