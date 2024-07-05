from flask import Blueprint, render_template, request, redirect, url_for
from Services.categoryServices import find_categories, update_category, delete_category
from Services.services import split_category_id

categories = Blueprint('categories', __name__)

@categories.route('/api/categories', methods=['GET'])
def get_category_ctrl():
    return find_categories()


@categories.route('/api/categories/<category_id>', methods=['PATCH'])
def update_category_ctrl(category_id):
    return update_category({
        "_id": split_category_id(category_id),
        "name": request.args.get("name"),
    })


@categories.route('/api/categories/<category_id>', methods=['DELETE'])
def delete_category_ctrl(category_id):
    return delete_category(category_id)


@categories.route('/view/categories', methods=['GET'])
def get_category_view():
    return render_template('get-categories.html', data=find_categories())

@categories.route('/view/categories/<category_id>', methods=['DELETE'])
def delete_category_view(category_id):
    delete_category(category_id)
    return redirect(url_for('categories.get_category_view'))


@categories.route('/view/categories/<category_id>', methods=['POST'])
def update_category_view(category_id):
    update_category({
        "_id": split_category_id(category_id),
        "name": request.form.get("name")
    })
    return redirect(url_for('categories.get_category_view'))


