from flask import Flask
import mysql.connector


app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a random secret key.



# Connect to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="strongPassword",
    database="todos"  # Replace with your database name
)
