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


def select_buffer_wav_data(conn, id):

    cursor = conn.cursor()

    sql = 'SELECT audio_buffer FROM wav_data WHERE id = ?'

    id = str(id)

    row = cursor.execute(sql, id).fetchone()

    return row

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

def select_config_by_name(conn):
    sql = "SELECT * FROM configs WHERE name= 'input_device'"

    cursor = conn.cursor()

    input = cursor.execute(sql).fetchone()

    return input



'''Função para criar tabelas'''

def create_tables(conn):

    cursor = conn.cursor()

    try:
        sql = "CREATE TABLE IF NOT EXISTS configs (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name VARCHAR(30), config VARCHAR(100));"
        cursor.execute(sql)

        print("Tabela configs criada com sucesso!")
    except Exception as e:
        print(e)

    try:
        sql = "CREATE TABLE IF NOT EXISTS wav_data (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT , nome VARCHAR(30) NOT NULL, data DATE,duracao INTEGER NOT NULL, image_path VARCHAR(50), audio_path VARCHAR(50), audio_buffer BLOB);"
        cursor.execute(sql)
        print("Tabela wave_data criada com sucesso!")
    except Exception as e:
        print(e)


def table_exists(conn):

    cursor = conn.cursor()

    sql = "SELECT EXISTS (SELECT name FROM sqlite_schema WHERE type='table' AND name='wav_data');"

    x = cursor.execute(sql).fetchone()

    return x 

'''Testando algumas paradas'''
import numpy as np
import json

conn = get_conn()

buffer = select_buffer_wav_data(conn, 1)



buffer = json.loads(buffer[0])

buffer = np.array(buffer)

buffer = buffer/10000


tamanho = np.size(buffer)

buffer_quadrado = buffer ** 2

soma = np.sum(buffer_quadrado)


media = soma/tamanho

raiz_quadrada_media = np.sqrt(media)

print(raiz_quadrada_media)

tempo = np.linspace(1, 100, 100)

print(tempo)




#buffer_quadrado = buffer ** 2




