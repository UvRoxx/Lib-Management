from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

import sqlite3
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
Bootstrap(app)
all_books = []

# project_dir = os.path.dirname(os.path.abspath(__file__))  # Getting the current project working dir
# database_file = "sqlite:///{}".format(os.path.join(project_dir, "books.db"))
# app.config['SQLALCHEMY_DATABASE_URI'] = database_file

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booksinfo.sqlite3'
db = SQLAlchemy(app)

# db = sqlite3.connect("books-collection.db")
# cursor = db.cursor()

app.config['SECRET_KEY'] = 'jsvksdfkjskndjfnksnfknsjkdnfjn'


# class Book(db.Model):
#     title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
#     author = db.Column(db.String(80), unique=False, nullable=False, primary_key=False)
#     rating = db.Column(db.Integer, unique=False, nullable=False, primary_key=False)
#
#     def __repr__(self):
#         return '<Title: {}>' % format(self.title)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column('title', db.String(80), nullable=False)
    author = db.Column('author', db.String(80), nullable=False)
    rating = db.Column(db.Integer(), nullable=False)

    def __init__(self, title, author, rating):
        self.title = title
        self.author = author
        self.rating = rating


db.create_all()


class BookForm(FlaskForm):
    title = StringField(label="Book Title:", validators=[DataRequired()])
    author = StringField(label="Book Author:", validators=[DataRequired()])
    rating = SelectField(label="Rating:", choices=(range(0, 10)), validators=[DataRequired()])
    submit = SubmitField(label="Add")


class RatingForm(FlaskForm):
    rating = SelectField(label="Rating:", choices=(range(0, 10)), validators=[DataRequired()])
    submit = SubmitField(label="Update Rating")


@app.route('/')
def home():
    return render_template("index.html", books=Book.query.all())


@app.route("/add", methods=['GET', 'POST'])
def add():
    book_form = BookForm()
    if book_form.validate_on_submit():
        book = {
            "title": book_form.title.data,
            "author": book_form.author.data,
            "rating": book_form.rating.data,
        }
        all_books.append(book)
        new_book = Book(book_form.title.data, book_form.author.data, book_form.rating.data)
        db.session.add(new_book)
        db.session.commit()
        print("added")
        return redirect(url_for('home'))
    return render_template("add.html", form=book_form)


@app.route("/edit/<book_id>", methods=['GET', 'POST'])
def edit_rating(book_id):
    book_to_update = Book.query.filter_by(id=book_id).first()
    edit_form = RatingForm()
    if edit_form.validate_on_submit():
        book_to_update.rating = edit_form.rating.data
        db.session.commit()
        print("Updated")
        return redirect(url_for("home"))
    return render_template("update_rating.html", book=book_to_update, form=edit_form)

@app.route('/delete/<book_id>')
def delete(book_id):
    book_to_delete = Book.query.filter_by(id=book_id).first()
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
