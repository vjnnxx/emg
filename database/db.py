import sqlite3
from sqlite3 import Error

def get_conn():
    try:
        conn = sqlite3.connect('emg.db')
    except Error as e:
        print(e)
    return conn

def select_all_wav_data(conn):
    cursor = conn.cursor()

    sql = 'SELECT * FROM wav_data'

    rows = cursor.execute(sql).fetchall()

    for row in rows:
        print(row)

def desc_wav_data(conn):
    cursor = conn.cursor()

    rows = cursor.execute("PRAGMA table_info('wav_data')").fetchall()


    for row in rows:
        print(row)

def create_wav_data(conn, wav_data):
    sql = "INSERT INTO wav_data(nome, data, duracao,image_path,audio_path, audio_buffer) VALUES (?, ?, ?, ?, ? ,?);"

    cursor = conn.cursor()

    cursor.execute(sql, wav_data)

    conn.commit()

    return cursor.lastrowid



def create_tables(conn):

    cursor = con.cursor()

    try:
        sql = "CREATE TABLE config (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT , config VARCHAR(100));"
        cursor.execute(sql)
        print("Tabela config criada com sucesso!")
    except Exception:
        print(Exception)

    try:
        sql = "CREATE TABLE wav_data (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT , nome VARCHAR(30) NOT NULL, data DATE,duracao INTEGER NOT NULL, image_path VARCHAR(50), audio_path VARCHAR(50), audio_buffer BLOB);"
        cursor.execute(sql)
        print("Tabela wave_data criada com sucesso!")
    except Exception:
        print(Exception)

con = get_conn()

select_all_wav_data(con)


