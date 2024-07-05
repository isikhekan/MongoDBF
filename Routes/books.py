from bson import ObjectId
from flask import Blueprint, render_template, redirect, request, url_for
from Services.bookServices import find_books, create_book, delete_book, update_book

books = Blueprint('books', __name__)


@books.route('/api/books', methods=['GET'])
def get_books_ctrl():
    return find_books()

@books.route('/api/books', methods=['POST'])
def create_book_ctrl():
    return create_book(
        request.json(),
        create_and_add=request.args.get('create_and_add')
    )


@books.route('/api/books/<book_id>', methods=['DELETE'])
def delete_book_ctrl(book_id):
    return delete_book(book_id)


@books.route('/api/books/<book_id>', methods=['PATCH'])
def update_book_ctrl(book_id):
    return update_book({
        "_id": ObjectId(book_id.split("/")[-1]),
        "title": request.args.get('title'),
        "creator": request.args.get('creator'),
        "content": request.args.get('content'),
    })


##SSR
@books.route('/view/books', methods=['GET'])
def get_books_view():
    return render_template('index.html', data={'books': find_books()})


@books.route('/view/books', methods=['POST'])
def create_book_view():
    create_book(
        {
            "category": request.form.get('category'),
            "title": request.form.get('title'),
            "creator": request.form.get('creator'),
            "content": request.form.get('content'),
        },
        create_and_add=request.form.get('create_and_add')
    )
    return render_template('index.html', data={'books': find_books()})


@books.route('/view/books/<book_id>', methods=['DELETE'])
def delete_book_view(book_id):
    delete_book(ObjectId(book_id))
    return redirect('/')

@books.route('/view/books/<book_id>', methods=['POST'])
def update_book_view(book_id):
    update_book(
        {
            "_id": ObjectId(book_id),
            "title": request.form.get('title'),
            "creator": request.form.get('creator'),
            "content": request.form.get('content'),
        }
    )
    return redirect(url_for('books.get_books_view'))
