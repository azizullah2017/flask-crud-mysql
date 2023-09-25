from config import mysql
from config import conn

def create_tables():
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            task TEXT,
            completed BOOLEAN DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    # cursor.commit()
    conn.commit()
    cursor.close()
