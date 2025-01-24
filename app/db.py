import psycopg2
import os

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscribers (
            user_id BIGINT PRIMARY KEY,
            language VARCHAR(2) DEFAULT 'ru',
            subscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stats (
            id SERIAL PRIMARY KEY,
            user_id BIGINT,
            command TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_subscriber(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO subscribers (user_id) VALUES (%s) ON CONFLICT (user_id) DO NOTHING', (user_id,))
    conn.commit()
    conn.close()

def remove_subscriber(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM subscribers WHERE user_id = %s', (user_id,))
    conn.commit()
    conn.close()

def get_subscribers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM subscribers')
    subscribers = cursor.fetchall()
    conn.close()
    return [sub[0] for sub in subscribers]

def log_command(user_id, command):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO stats (user_id, command) VALUES (%s, %s)', (user_id, command))
    conn.commit()
    conn.close()
