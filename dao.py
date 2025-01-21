import json
import os.path
import sqlite3


def connect(path):
    exists = os.path.exists(path)
    __conn = sqlite3.connect(path)
    if not exists:
        create_tables(__conn)
    __conn.row_factory = sqlite3.Row
    return __conn


def create_tables(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS carts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            contents TEXT,
            cost REAL
        )
    ''')
    conn.commit()


def get_cart(username: str) -> list:
    conn = connect('carts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT contents FROM carts WHERE username = ?', (username,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    if row is None:
        return []
    return json.loads(row['contents'])


def add_to_cart(username: str, product_id: int):
    conn = connect('carts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT contents FROM carts WHERE username = ?', (username,))
    row = cursor.fetchone()
    if row is None:
        contents = []
        cursor.execute('INSERT INTO carts (username, contents, cost) VALUES (?, ?, ?)',
                       (username, json.dumps(contents), 0))
    else:
        contents = json.loads(row['contents'])
    
    contents.append(product_id)
    cursor.execute('UPDATE carts SET contents = ? WHERE username = ?',
                   (json.dumps(contents), username))
    conn.commit()
    cursor.close()
    conn.close()


def remove_from_cart(username: str, product_id: int):
    conn = connect('carts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT contents FROM carts WHERE username = ?', (username,))
    row = cursor.fetchone()
    if row is None:
        cursor.close()
        conn.close()
        return
    
    contents = json.loads(row['contents'])
    if product_id in contents:
        contents.remove(product_id)
        cursor.execute('UPDATE carts SET contents = ? WHERE username = ?',
                       (json.dumps(contents), username))
        conn.commit()
    
    cursor.close()
    conn.close()


def delete_cart(username: str):
    conn = connect('carts.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM carts WHERE username = ?', (username,))
    conn.commit()
    cursor.close()
    conn.close()
