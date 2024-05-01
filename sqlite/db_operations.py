import sqlite3
import os
import time


def insert_data(status: str, text: str, file: str, video: str, reasons: str):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_folder = os.path.join(current_dir, '../sqlite')
    db_file = os.path.join(db_folder, 'posts.db')

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute('''INSERT INTO posts (status, text, file, video, reasons, unix_timestamp) VALUES (?, ?, ?, ?, ?, ?)''', (status, text, file, video, reasons, int(time.time())))
    
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
        "video": video_path
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
        results.append({'id': row[0], 'status': row[1], 'comment': row[2], 'image': row[3], 'video': row[4], 'reasons': row[5], 'unix_timestamp': row[6]})
    
    conn.close()

    return results


if __name__ == "__main__":
    conn = sqlite3.connect('posts.db')
    cursor = conn.cursor()


    conn.commit()
    conn.close()
   