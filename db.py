import sqlite3

def create_db():
    # Creating users.db file
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Creating USERS table.
    cursor.execute('''CREATE TABLE IF NOT EXISTS USERS (
        name TEXT, 
        chat_id INTEGER
        )
    ''')

    # Creating ADMINS table.
    cursor.execute('''CREATE TABLE IF NOT EXISTS ADMINS (
        name TEXT,
        admin_id INTEGER
    )
    ''')


    conn.commit()
    conn.close()