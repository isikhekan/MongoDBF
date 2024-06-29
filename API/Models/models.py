from bson import json_util, ObjectId
from Database.database import create_db

collections = create_db()
books = collections['books']
categories = collections['categories']


def api_show_categories():
    return json_util.dumps(categories.find())


def api_update_category(category_id, request):
    category_id = category_id.split("/")[-1]
    if categories.find_one({"_id": ObjectId(category_id)}) == None:
        return {
            'error': 'this category id does not exist'
        }
    filter = {'_id': ObjectId(category_id)}
    old_category_details = categories.find_one(filter)
    newCategoryName = request.args.get('name')
    categories.find_one_and_update(filter, {'$set': {"name": newCategoryName}})
    return {
        'success': True,
        'old_category_name': json_util.dumps(old_category_details),
        'new_category_name': json_util.dumps(categories.find(filter)),
        'Message': 'Updated successfully'
    }


def api_delete_category(category_id):
    if categories.find_one({"_id": ObjectId(category_id)}) == None:
        return {
            'success': False,
            'error': 'this category id does not exist'
        }
    if books.find_one({'category_id': ObjectId(category_id)}) != None:
        return {
            'success': False,
            'error': 'this category has book(s)'
        }
    categories.delete_one({'_id': ObjectId(category_id)})
    return {
        'success': True,
        'Message': 'Category deleted successfully',
        'Exist categories': json_util.dumps(categories.find())
    }
