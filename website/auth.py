# website/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app

auth = Blueprint('auth', __name__)

def check_admin_login(username, password):
    """Verifica se o usuário e senha fornecidos coincidem com os dados do administrador descriptografados."""
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
            return redirect(url_for('views.home'))
        else:
            flash('Login inválido. Tente novamente.')

    return render_template("login.html")

@auth.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('auth.login'))
