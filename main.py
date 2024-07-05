from flask import Flask
from Routes.books import books
from Routes.categories import categories

app = Flask(__name__)
app.register_blueprint(books)
app.register_blueprint(categories)

if '__name__':
    app.run(debug=True)
