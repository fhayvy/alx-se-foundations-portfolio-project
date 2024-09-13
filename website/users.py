from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

users = Blueprint('users', __name__)

@users.route('/')
def index():
    return render_template('index.html', user=current_user)

@users.route('/profiles')
def profiles():
    return "<p>List of Users</p>"


@users.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash(f'Welcome {user.first_name}', category='success')
                return redirect(url_for('users.index'))

            else:
                print("Incorrect password")
        else:
            print("Email does not exist")

    return render_template('login.html', user=current_user)


@users.route('/create', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        email = request.form.get('email')
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists, please use a different email', category='error')
        
        # Validation Logic
        if not email or not first_name or not last_name or not password1 or not password2:
            flash('All fields are required!', category='error')
            pass
        elif password1 != password2:
            flash('Passwords do not match!', category='error')
            pass
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=generate_password_hash(password1, method='pbkdf2:sha256')
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created", category='success')
            # flash(f'Welcome {first_name}', success)
            return redirect(url_for('users.index'))
    return render_template('sign-up.html', user=current_user)
    

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.login'))