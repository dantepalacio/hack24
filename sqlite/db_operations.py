import sqlite3
import os
import time


def insert_data(status: str, text: str, file: str, video: str, reasons: str, action: int=None):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_folder = os.path.join(current_dir, '../sqlite')
    db_file = os.path.join(db_folder, 'posts.db')

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute('''INSERT INTO posts (status, text, file, video, reasons, unix_timestamp, action) VALUES (?, ?, ?, ?, ?, ?, ?)''', (status, text, file, video, reasons, int(time.time()), action))
    
    conn.commit()
    conn.close()


def delete_data(id: int):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_folder = os.path.join(current_dir, '../sqlite')
    db_file = os.path.join(db_folder, 'posts.db')

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute('''DELETE FROM posts WHERE id = ?''', (id,))
    
    conn.commit()
    conn.close()


def get_post_id(status: str, text: str, image_path: str, video_path: str, reasons: str) -> int:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_folder = os.path.join(current_dir, '../sqlite')
    db_file = os.path.join(db_folder, 'posts.db')

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    search_params = {
        "text": text,
        "file": image_path,
        "reasons": reasons,
        "status": status,
        "video": video_path,
    }

    query = "SELECT id FROM posts WHERE "
    conditions = []

    for key, value in search_params.items():
        if value is None:
            conditions.append(f"{key} IS NULL")
        else:
            conditions.append(f"{key} = ?")

    query += " AND ".join(conditions)

    cursor.execute(query, [v for v in search_params.values() if v is not None])
    result = cursor.fetchone()

    conn.close()
    
    return result[0]


def get_post_by_id(id:int) -> dict:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_folder = os.path.join(current_dir, '../sqlite')
    db_file = os.path.join(db_folder, 'posts.db')

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()


    cursor.execute('SELECT * FROM posts WHERE id=?', (id,))
    result = cursor.fetchone()

    conn.close()

    answer = ({'id': result[0], 'status': result[1], 'comment': result[2], 'image': result[3], 'video': result[4], 'reasons': result[5], 'unix_timestamp': result[6], 'action': result[7]})
    
    return answer

def get_table():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_folder = os.path.join(current_dir, '../sqlite')
    db_file = os.path.join(db_folder, 'posts.db')

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute('''SELECT * FROM posts''')
    
    rows = cursor.fetchall()
    
    results = []

    for row in rows:
        results.append({'id': row[0], 'status': row[1], 'comment': row[2], 'image': row[3], 'video': row[4], 'reasons': row[5], 'unix_timestamp': row[6], 'action': row[7]})
    
    conn.close()

    return results


ACTIONS = ['dislike','like']
def set_action(action,id):
    print('AAAA')
    print(action)
    print(id)
    print(ACTIONS.index(action))

    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_folder = os.path.join(current_dir, '../sqlite')
    db_file = os.path.join(db_folder, 'posts.db')

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute('''UPDATE posts SET action=? WHERE id=?''',(ACTIONS.index(action),int(id)))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()

    # cursor.execute('''DROP TABLE posts''')

    # cursor.execute('''CREATE TABLE posts (id INTEGER PRIMARY KEY, status CHAR, text CHAR, file CHAR, video CHAR, reasons CHAR, unix_timestamp INTEGER, action INTEGER)''')
    # cursor.execute('''INSERT INTO posts (status, text, file, video, reasons, unix_timestamp, action) VALUES (?, ?, ?, ?, ?, ?, ?)''', ('publish', 'hello', None, None, '', int(time.time()), 1))

    conn.commit()
    conn.close()
   