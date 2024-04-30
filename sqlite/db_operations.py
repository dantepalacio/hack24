import sqlite3
import os


def insert_data(id: int, status: str, text: str, file: str, video: str, reasons: str):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_folder = os.path.join(current_dir, '../sqlite')
    db_file = os.path.join(db_folder, 'posts.db')

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute('''INSERT INTO data (id, status, text, file, video, reasons) VALUES (?, ?, ?, ?, ?, ?)''', (id, status, text, file, video, reasons,))
    
    conn.commit()
    conn.close()


def delete_data(id: int):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_folder = os.path.join(current_dir, '../sqlite')
    db_file = os.path.join(db_folder, 'posts.db')

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute('''DELETE FROM data WHERE id = ?''', (id,))
    
    conn.commit()
    conn.close()


def view_table():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_folder = os.path.join(current_dir, '../sqlite')
    db_file = os.path.join(db_folder, 'posts.db')

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute('''SELECT * FROM data''')
    
    rows = cursor.fetchall()
    
    for row in rows:
        print(row)
    
    conn.close()


if __name__ == "__main__":
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()

    # cursor.execute('''CREATE TABLE data (id int primary key, status char, text char, file char, video char, reasons char)''')
    # cursor.execute('''INSERT INTO data (id, status, text, file, video, reasons) VALUES (?, ?, ?, ?, ?, ?)''', (1, 'ban', 'text', '1.jpg', '1.mp4', 'poshel nahui'))
    insert_data(2, 'publish', 'text', '2.jpg', '2.mp4', 'norm')
    view_table()

    conn.commit()
    conn.close()

    # view_table()
   