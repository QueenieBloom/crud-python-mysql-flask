from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from .models import connect

# Create a Blueprint for views
views = Blueprint('views', __name__)

@views.route('/')
def home():
    """Render the home page."""
    return render_template("home.html")

@views.route('/add_user', methods=['POST'])
def add_user():
    """Add a new user to the database."""
    # Retrieve JSON data from the request
    data = request.get_json()
    conn = connect()  # Establish a database connection
    cursor = conn.cursor()  # Create a cursor object for executing SQL commands

    # Check if the email is already registered
    cursor.execute("SELECT * FROM users WHERE email = %s", (data['email'],))
    if cursor.fetchone():  # If an email is found, return an error
        flash("Email already registered!", "error")
        return jsonify({"redirect": url_for('views.home')}), 400

    # Check if the username is already registered
    cursor.execute("SELECT * FROM users WHERE username = %s", (data['username'],))
    if cursor.fetchone():  # If a username is found, return an error
        flash("Username already registered!", "error")
        return jsonify({"redirect": url_for('views.home')}), 400

    # Add the new user to the database
    cursor.execute("""
        INSERT INTO users (firstName, lastName, username, email, password)
        VALUES (%s, %s, %s, %s, %s)
    """, (data['firstName'], data['lastName'], data['username'], data['email'], data['password']))
    conn.commit()  # Commit the changes to the database
    cursor.close()  # Close the cursor
    conn.close()  # Close the database connection
    flash("User added successfully!", "success")  # Display a success message
    return jsonify({"redirect": url_for('views.home')})  # Redirect to home page

@views.route('/update_user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an existing user's information."""
    # Retrieve JSON data from the request
    data = request.get_json()
    conn = connect()  # Establish a database connection
    cursor = conn.cursor()  # Create a cursor object

    # Check if the email is already registered, excluding the current user
    cursor.execute("SELECT * FROM users WHERE email = %s AND id != %s", (data['email'], user_id))
    if cursor.fetchone():  # If an email is found, return an error
        flash("Email already registered!", "error")
        return jsonify({"redirect": url_for('views.home')}), 400

    # Check if the username is already registered, excluding the current user
    cursor.execute("SELECT * FROM users WHERE username = %s AND id != %s", (data['username'], user_id))
    if cursor.fetchone():  # If a username is found, return an error
        flash("Username already registered!", "error")
        return jsonify({"redirect": url_for('views.home')}), 400

    # Update the user's information in the database
    cursor.execute("""
        UPDATE users SET firstName = %s, lastName = %s, username = %s, email = %s, password = %s
        WHERE id = %s
    """, (data['firstName'], data['lastName'], data['username'], data['email'], data['password'], user_id))
    conn.commit()  # Commit the changes to the database
    cursor.close()  # Close the cursor
    conn.close()  # Close the database connection
    flash("User updated successfully!", "success")  # Display a success message
    return jsonify({"redirect": url_for('views.home')})  # Redirect to home page

@views.route('/get_user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve a user's information by user ID."""
    conn = connect()  # Establish a database connection
    cursor = conn.cursor(dictionary=True)  # Create a cursor object with dictionary output
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()  # Fetch the user record
    cursor.close()  # Close the cursor
    conn.close()  # Close the database connection
    if user:
        return jsonify({"user": user})  # Return user data if found
    else:
        flash("User not found!", "error")  # Display an error message if user not found
        return jsonify({"redirect": url_for('views.home')}), 404  # Redirect to home page

@views.route('/get_users', methods=['GET'])
def get_users():
    """Retrieve a list of all users."""
    conn = connect()  # Establish a database connection
    cursor = conn.cursor(dictionary=True)  # Create a cursor object with dictionary output
    cursor.execute("SELECT * FROM users")  # Query to get all users
    users = cursor.fetchall()  # Fetch all user records
    cursor.close()  # Close the cursor
    conn.close()  # Close the database connection
    return jsonify({"users": users})  # Return the list of users

@views.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user by user ID."""
    conn = connect()  # Establish a database connection
    cursor = conn.cursor()  # Create a cursor object
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))  # Execute delete query
    conn.commit()  # Commit the changes to the database
    cursor.close()  # Close the cursor
    conn.close()  # Close the database connection
    flash("User deleted successfully!", "success")  # Display a success message
    return jsonify({"redirect": url_for('views.home')})  # Redirect to home page

@views.route('/settings')
def settings():
    """Render the settings page."""
    return render_template('settings.html')

