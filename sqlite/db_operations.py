import sqlite3


def insert_data(text: str, file: str, status: str):
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()
    
    cursor.execute('''INSERT INTO posts (text, file, status) VALUES (?, ?, ?)''', (text, file, status))
    
    conn.commit()
    conn.close()


def delete_data(id: int):
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()
    
    cursor.execute('''DELETE FROM posts WHERE id = ?''', (id,))
    
    conn.commit()
    conn.close()


def view_table():
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()
    
    cursor.execute('''SELECT * FROM posts''')
    
    rows = cursor.fetchall()
    
    for row in rows:
        print(row)
    
    conn.close()


if __name__ == "__main__":
    view_table()
   