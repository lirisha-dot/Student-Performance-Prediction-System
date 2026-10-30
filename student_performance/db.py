import mysql.connector

CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",   # <-- change this
    "database": "student_db",
}

def get_conn():
    return mysql.connector.connect(**CONFIG)
