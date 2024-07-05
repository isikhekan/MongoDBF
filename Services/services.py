from Database.database import create_db
collections = create_db()
books = collections['books']
categories = collections['categories']


def split_category_id(data):
    return data.split("/")[-1]

def find_book(key,value):
    return books.find_one({key:value})



