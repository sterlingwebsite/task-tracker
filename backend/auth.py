from werkzeug.security import check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import add_user, get_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        if user and check_password_hash(user[2], password):  # user[2] is the password column
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('tasks.dashboard'))
        flash("Invalid username or password")
        return redirect(url_for('auth.login'))
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if get_user(username):
            flash("Username already exists")
            return redirect(url_for('auth.register'))
        add_user(username, password)
        flash("Registration successful. Please log in.")
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('auth.login'))
