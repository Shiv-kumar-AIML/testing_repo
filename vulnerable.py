import os
import sqlite3

def login(username, password):
    # SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.execute(query)
    return cursor.fetchone()

def run_command(user_input):
    # Command injection vulnerability  
    os.system(f"echo {user_input}")


def unsafe_eval(user_input):
    # Code injection vulnerability
    return eval(user_input)

def read_file(filename):
    # Path traversal vulnerability
    return open(f"/data/{filename}").read()
