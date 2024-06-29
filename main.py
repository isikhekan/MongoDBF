from flask import Flask, request, render_template, url_for, redirect
from bson import json_util
from Routes.routes import db_add_book, db_del_book, db_update_book
from API.Routes.routes import api_add_book, api_del_book, api_update_book, api_get_books
from API.Models.models import api_show_categories, api_update_category, api_delete_category
from Models.models import show_categories
from Database.database import create_db
from Models.models import simple_page

app = Flask(__name__)
app.register_blueprint(simple_page)
collections = create_db()
books = collections['books']
categories = collections['categories']


@app.route('/', methods=('GET', 'POST'))
def index():
    all_books = books.find()
    return render_template('index.html', data={'all_books': json_util.dumps(all_books)})


@app.route('/add', methods=('GET', 'POST'))
def add_book():
    return db_add_book(request)


@app.route('/delete/<book_id>', methods=('GET', 'POST', 'DELETE'))
def delete_book(book_id):
    db_del_book(book_id)
    return redirect(url_for('index'))


@app.route('/update/<book_id>', methods=('GET', 'POST', 'PATCH', 'PUT'))
def update_book(book_id):
    db_update_book(book_id, request)
    return redirect(url_for('index'))


@app.route('/categories', methods=('GET', 'POST'))
def show_categories_page():
    return show_categories()


##API kısmı

@app.route('/api/books', methods=('GET', 'POST'))
def api_books_page():
    return api_get_books()


@app.route('/api/add', methods=('GET', 'POST'))
def api_add_page():
    return api_add_book(request)


@app.route('/api/delete/<book_id>', methods=('GET', 'POST', 'DELETE'))
def api_delete_page(book_id):
    return api_del_book(book_id)


@app.route('/api/update/<book_id>', methods=('GET', 'POST', 'PATCH'))
def api_update_page(book_id):
    return api_update_book(book_id, request)


@app.route('/api/categories/categories')
def api_categories_page():
    return api_show_categories()


@app.route('/api/categories/update/<category_id>')
def api_update_category_page(category_id):
    return api_update_category(category_id, request)


@app.route('/api/categories/delete/<category_id>', methods=('GET', 'POST'))
def api_delete_category_page(category_id):
    return api_delete_category(category_id)


if '__name__':
    app.run(debug=True)
