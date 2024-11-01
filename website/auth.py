from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    data = request.form
    print(data)
    return render_template('login.html', boolean=True)

@auth.route('/logout')
def logout():
    return '<p>Logout<p>'

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')

        if len(firstName) < 3 or len(lastName) < 3:
            flash('Fist Name or Last Name has less than 3 characters.', category='error')
        elif len(username) < 4: 
            flash('Username must be longer than 4 characters', category='error')
        elif len(password) < 5:
            flash('Username must be longer than 5 characters', category='error')
        elif len(email) < 10:
            flash('email must be longer than 10 characters', category='error')
        elif password != confirmPassword:
            flash('Passwords don\'t match!', category='error') 
        else:
            flash('Account created!', category='sucess')
         
    return render_template('sign-up.html')