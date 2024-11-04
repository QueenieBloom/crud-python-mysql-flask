# website/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app

auth = Blueprint('auth', __name__)

def check_admin_login(username, password):
    """Checks if the provided username and password match the decrypted admin credentials."""
    admin_username = current_app.config['ADMIN_USERNAME']
    admin_password = current_app.config['ADMIN_PASSWORD']

    return username == admin_username and password == admin_password

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if check_admin_login(username, password):
            session['admin_logged_in'] = True
            session['username'] = username
            return redirect(url_for('views.home'))
        else:
            flash('Invalid login. Please try again.')

    return render_template("login.html")

@auth.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    session.pop('username', None)
    return redirect(url_for('auth.login'))
