import sqlite3
from sqlite3 import Error

def get_conn():
    try:
        conn = sqlite3.connect('emg.db')
    except Error as e:
        print(e)
    return conn


'''Operações da tabela wav_data'''
def select_all_wav_data(conn):
    cursor = conn.cursor()

    sql = 'SELECT id, nome, data, duracao, image_path, audio_path FROM wav_data'

    rows = cursor.execute(sql).fetchall()
    
    return rows

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

'''Operações da tabela configs'''

def create_config(conn, config):
    

    sql_delete = "DELETE FROM configs"

    cursor = conn.cursor()

    cursor.execute(sql_delete)

    conn.commit()


    sql_insert = "INSERT INTO configs(name, config) VALUES (?, ?);"

    

    cursor.execute(sql_insert, config)

    conn.commit()

    return cursor.lastrowid

def selec_config_by_name(conn):
    sql = "SELECT * FROM configs WHERE name= 'input_device'"

    cursor = conn.cursor()

    input = cursor.execute(sql).fetchone()

    return input



'''Função para criar tabelas'''

def create_tables(conn):

    cursor = con.cursor()

    try:
        sql = "CREATE TABLE configs (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name VARCHAR(30), config VARCHAR(100));"
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

config = ('input_device', '{"id": 1}')

create_config(con, config)





