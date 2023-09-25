from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
from models import create_tables
from config import app, conn
# Initialize the database tables
# create_tables()


# Create a cursor object to interact with the database
cursor = conn.cursor()

app.secret_key = "your_secret_key"  # Change this to a random secret key.

# Import necessary modules
from werkzeug.security import generate_password_hash, check_password_hash

# Route for checking and updating user profile
@app.route('/api/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' in session:
        cursor = conn.cursor(dictionary=True)

        if request.method == 'POST':
            # Handle password update
            current_password = request.form['current_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']

            cursor.execute("SELECT password FROM users WHERE id = %s", (session['user_id'],))
            user = cursor.fetchone()

            if user and check_password_hash(user['password'], current_password):
                if new_password == confirm_password:
                    # Update the user's password
                    hashed_password = generate_password_hash(new_password)
                    cursor.execute("UPDATE users SET password = %s WHERE id = %s", (hashed_password, session['user_id']))
                    conn.commit()
                    flash('Password updated successfully', 'success')
                else:
                    flash('New password and confirm password do not match', 'danger')
            else:
                flash('Current password is incorrect', 'danger')

        cursor.execute("SELECT username FROM users WHERE id = %s", (session['user_id'],))
        user = cursor.fetchone()
        # cursor.close()

        return render_template('profile.html', username=user['username'])
    else:
        flash('You must be logged in to access your profile', 'danger')
        return redirect(url_for('login'))


@app.route('/api/')
def index():
    if 'user_id' in session:
        print(" index page")
        # Fetch user-specific todos from the database
        cursor.execute("SELECT * FROM todos WHERE user_id = %s", (session['user_id'],))
        todos = cursor.fetchall()
        print(todos)
        return render_template('todos.html', todos=todos)
    return render_template('login.html')

@app.route('/api/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validate passwords match
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('signup.html')

        # Check if the username already exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Username already exists', 'danger')
            return render_template('signup.html')

        # Insert the new user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()

        flash('You are now registered and can log in', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        if user and user[2] == password:
            session['user_id'] = user[0]
            print(" successful login")
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your username and password.', 'danger')

    return render_template('login.html')

@app.route('/api/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/api/todos/add', methods=['POST'])
def add_todo():
    if 'user_id' in session:
        task = request.form['task']
        cursor.execute("INSERT INTO todos (user_id, task) VALUES (%s, %s)", (session['user_id'], task))
        conn.commit()
        flash('Todo added successfully', 'success')
    else:
        flash('You must be logged in to add a todo', 'danger')

    return redirect(url_for('index'))


@app.route('/api/todos/<int:id>/edit', methods=['GET', 'POST'])
def edit_todo(id):
    if 'user_id' in session:
        if request.method == 'POST':
            task = request.form['task']
            cursor.execute("UPDATE todos SET task = %s WHERE id = %s AND user_id = %s",
                           (task, id, session['user_id']))
            conn.commit()
            return redirect(url_for('index'))
        else:
            cursor.execute("SELECT * FROM todos WHERE id = %s AND user_id = %s", (id, session['user_id']))
            todo = cursor.fetchone()
            return render_template('edit_todo.html', todo=todo)
    return redirect(url_for('index'))

@app.route('/api/todos/<int:id>/delete', methods=['POST'])
def delete_todo(id):
    if 'user_id' in session:
        cursor.execute("DELETE FROM todos WHERE id = %s AND user_id = %s", (id, session['user_id']))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
