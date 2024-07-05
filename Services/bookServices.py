from Services.categoryServices import find_category, create_category
from datetime import datetime
from bson import json_util, ObjectId
from Database.database import create_db
from Models.bookModel import Book

collections = create_db()
books = collections['books']


def find_books():
    found_books = books.find()
    return json_util.dumps([Book.from_dict(book).to_dict() for book in found_books])

def create_book(book_data, **kwargs):
    created_at = datetime.now()
    category_is_exist = find_category({'name': book_data['category']})
    if category_is_exist == None:
        if kwargs.get("create_and_add") == None:
            return {
                'success': False,
                'message': 'You must add category before adding book'
            }
        create_category({'name': book_data['category']})
    category_id = find_category({'name': book_data['category']})['_id']
    new_book = Book(created_at=created_at, category_id=category_id, **book_data)
    books.insert_one(
        new_book.to_dict(id=False)
    )
    return {
        'success': True,
        'message': 'Book created'
    }


def delete_book(book_id):
    books.delete_one({'_id': ObjectId(book_id)})
    return {
        'success': True
    }


def update_book(book_data):
    filter = {"_id": book_data['_id']}
    new_values = {"$set":
        {
            'title': book_data['title'],
            'creator': book_data['creator'],
            'content': book_data['content'],
            'created_at': datetime.now()
        }}
    books.find_one_and_update(filter, new_values)
    return {
        'success': True
    }
