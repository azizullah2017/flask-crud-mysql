from flask import Flask
# from flask_mysqldb import MySQL
import mysql.connector


app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a random secret key.

# # MySQL Configuration
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'Azizullah@!321'
# app.config['MYSQL_DB'] = 'todos'
# mysql = MySQL(app)

# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Azizullah@!321",
    database="todos"  # Replace with your database name
)

# # Create a cursor object to interact with the database
# cursor = conn.cursor()