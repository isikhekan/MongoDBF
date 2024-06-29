import datetime
from bson import json_util, ObjectId
from Models.models import add_book, get_books
from Database.database import create_db

collections = create_db()
books = collections['books']
categories = collections['categories']


def api_get_books():
    return json_util.dumps(books.find())


def api_add_book(request):
    category = request.args.get('category')
    title = request.args.get('title')
    creator = request.args.get('creator')
    content = request.args.get('content')
    created_at = datetime.datetime.now()
    if request.args.get('createnadd'):
        if categories.find_one({'name': category}) == None:
            categories.insert_one({'name': category})
        category = categories.find_one({'name': category})
        category_id = category['_id']
        add_book(title, creator, content, created_at, category_id)
        return json_util.dumps(get_books())
    else:
        if categories.find_one({'name': category}) != None:
            category_id = categories.find_one({'name': category})['_id']
            add_book(title, creator, content, created_at, category_id)
            return json_util.dumps(get_books())
        return {
            'error': 'You must add category before adding book to this category'
        }


def api_del_book(book_id):
    books.delete_one({'_id': ObjectId(book_id)})
    return {'success': True, 'message': 'Book deleted successfully'}


def api_update_book(book_id, request):
    book_id = book_id.split("/")[-1]
    filter = {"_id": ObjectId(book_id)}
    before_update = books.find_one(filter)
    new_values = {"$set":
        {
            'title': request.args.get('title'),
            'creator': request.args.get('creator'),
            'content': request.args.get('content'),
            'created_at': datetime.datetime.now()
        }}
    books.find_one_and_update(filter, new_values)
    return {
        'success': True,
        'old': json_util.dumps(before_update),
        'new': json_util.dumps(books.find_one(filter))
    }
