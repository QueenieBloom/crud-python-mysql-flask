# website/views.py
from flask import Blueprint, render_template, session, redirect, url_for

views = Blueprint('views', __name__)

@views.route('/')
def home():
    if not session.get('admin_logged_in'):
        return redirect(url_for('auth.login'))
    return render_template("home.html")
