from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import Books
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/create', methods=['POST'])
def create():
    book_title = request.form.get('title')
    book_author = request.form.get('author')
    new_book = Books(title=book_title, author=book_author, read=False, user_id = current_user.id) 
    db.session.add(new_book)
    db.session.commit()

    return redirect(url_for('views.home'))

@auth.route('/delete/<int:book_id>')
def delete(book_id):
    book_delete = Books.query.filter_by(id = book_id).first()
    db.session.delete(book_delete)
    db.session.commit()
    return redirect(url_for('views.home'))

@auth.route('/update/<int:book_id>', methods=['POST'])
def update_book(book_id):
    new_title = request.form.get('new_title')
    new_author = request.form.get('new_author')
    book_update = Books.query.filter_by(id = book_id).first()
    book_update.title = new_title
    book_update.author = new_author
    db.session.commit()
    return redirect(url_for('views.home'))


@auth.route('/change-status/<int:book_id>')
def change_status(book_id):
    book_status = Books.query.filter_by(id=book_id).first()
    book_status.read = not book_status.read
    db.session.commit()
    return redirect(url_for('views.home'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))



@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(username) < 2:
            flash('Username must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
            

    
