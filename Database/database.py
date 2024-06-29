from flask import Flask, request, render_template, url_for, redirect, Response, jsonify
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.book_database
categories = db.categories
books = db.books

def create_db():
    return {
        'books': books,
        'categories': categories,
    }
