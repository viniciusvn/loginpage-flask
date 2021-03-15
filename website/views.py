from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Books
from .models import User
views = Blueprint('views', __name__)



@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user, username= current_user.username)

@views.route('/books')
@login_required
def books():
    book_list = Books.query.filter_by(user_id = current_user.id).all()
    return render_template("books.html", user=current_user, book_list=book_list, username= current_user.username)
