from Models.categoryModel import Category
from Services.services import find_book
from bson import json_util, ObjectId
from Database.database import create_db

collections = create_db()
categories = collections['categories']


def find_categories():
    found_categories = categories.find()
    return json_util.dumps([Category.from_dict(category).to_dict() for category in found_categories])


def create_category(category_data):
    categories.insert_one(
        {
            'name': category_data['name'],
        })
    return {
        'success': True
    }


def update_category(category_data):
    filter = {'_id': ObjectId(category_data['_id'])}
    categories.find_one_and_update(filter, {
        '$set': {"name": category_data['name']}
    })
    return {
        'success': True
    }

def delete_category(category_id):
    if find_book('category_id', ObjectId(category_id)) == None:
        categories.delete_one({'_id': ObjectId(category_id)})
        return {
            'success': True,
            'message': 'Successfully deleted category'
        }
    return {
        'success': False,
        'message': 'You must delete whole books connected by this category'
    }


def find_category(data):
    return categories.find_one({list(data.keys())[0]: next(iter(data.values()))})
