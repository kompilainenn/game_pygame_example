import sqlite3

def init_db():
    conn = sqlite3.connect('game_results.db')  # Создаем или подключаемся к БД
    cursor = conn.cursor()
    
    # Создаем таблицу, если она не существует
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_name TEXT NOT NULL,
        score INTEGER NOT NULL        
    )
    ''')
    
    # Проверяем, пустая ли таблица
    cursor.execute('SELECT COUNT(*) FROM results')
    count = cursor.fetchone()[0]
    
    # Если таблица пуста, добавляем начальные данные
    if count == 0:
        initial_data = [
            ('Uporoty', 1000),
            ('Hard_player', 850),
            ('JustGrimzy', 125),
            ('A-la Banda', 500),
            ('Kolyan', 5)
        ]
        cursor.executemany('INSERT INTO results (player_name, score) VALUES (?, ?)', initial_data)
    
    conn.commit()
    conn.close()

def add_result(player_name, score):
    conn = sqlite3.connect('game_results.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO results (player_name, score)
    VALUES (?, ?)
    ''', (player_name, score))
    
    conn.commit()
    conn.close()

def get_results():
    conn = sqlite3.connect('game_results.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT player_name, score FROM results ORDER BY score DESC LIMIT 5')
    results = cursor.fetchall()
    
    conn.close()
    return results