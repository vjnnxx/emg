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

def select_wav_data(conn, id):

    cursor = conn.cursor()

    sql = 'SELECT nome, duracao, image_path, audio_path, sample_rate FROM wav_data WHERE id = ?;'

    id = str(id)

    row = cursor.execute(sql, [id]).fetchone()


    return row


def select_buffer_wav_data(conn, id):

    cursor = conn.cursor()

    sql = 'SELECT audio_buffer FROM wav_data WHERE id = ?'

    id = str(id)

    row = cursor.execute(sql, [id]).fetchone()

    return row

def desc_wav_data(conn):
    cursor = conn.cursor()

    rows = cursor.execute("PRAGMA table_info('wav_data')").fetchall()


    for row in rows:
        print(row)

def create_wav_data(conn, wav_data):
    sql = "INSERT INTO wav_data(nome, data, duracao,image_path,audio_path, audio_buffer, sample_rate) VALUES (?, ?, ?, ?, ? ,?, ?);"

    cursor = conn.cursor()

    cursor.execute(sql, wav_data)

    conn.commit()

    return cursor.lastrowid

def delete_wav_data(conn, id):

    sql = "DELETE FROM wav_data WHERE id = ?"

    cursor = conn.cursor()

    id = str(id)

    cursor.execute(sql, [id])

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

def select_config_input_device(conn):
    sql = "SELECT * FROM configs WHERE name= 'input_device'"

    cursor = conn.cursor()

    input = cursor.execute(sql).fetchone()

    return input


'''Operações da tabela pessoas'''

def select_all_pessoas(conn):
    cursor = conn.cursor()

    sql = 'SELECT PessoaID, nome, data_nasc FROM pessoas;'

    rows = cursor.execute(sql).fetchall()
    
    return rows

def create_pessoa(conn, pessoa):

    cursor = conn.cursor()

    sql = 'INSERT INTO pessoas (nome, data_nasc, observacoes) VALUES (?, ?, ?);'

    cursor.execute(sql,pessoa)

    conn.commit()

    return cursor.lastrowid

'''Operações da tabela analises'''

def get_analise_by_id_individuo(conn, id):

    cursor = conn.cursor()

    sql = 'SELECT AnaliseID, nome FROM analises WHERE PessoaID = ?'

    id = str(id)

    rows = cursor.execute(sql, [id]).fetchall()

    return rows



'''Função para criar tabelas'''

def create_tables(conn):

    cursor = conn.cursor()

    #configs
    try:
        sql = "CREATE TABLE IF NOT EXISTS configs (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name VARCHAR(30), config VARCHAR(100));"
        cursor.execute(sql)

        print("Tabela configs criada com sucesso!")
    except Exception as e:
        print(e)



    #wav_data
    try:
        sql = "CREATE TABLE IF NOT EXISTS wav_data (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT , nome VARCHAR(30) NOT NULL, data DATE,duracao INTEGER NOT NULL, image_path VARCHAR(50), audio_path VARCHAR(50), audio_buffer BLOB, sample_rate INTEGER NOT NULL);"
        cursor.execute(sql)
        print("Tabela wave_data criada com sucesso!")
    except Exception as e:
        print(e)


    #pessoas

    try:
        sql = "CREATE TABLE IF NOT EXISTS pessoas (PessoaID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, nome VARCHAR(30), data_nasc DATE, observacoes TEXT);"
        cursor.execute(sql)
        print("Tabela pessoas criada com sucesso!")
    except Exception as e:
        print(e)


    #analises
        
    try: 
        sql = "CREATE TABLE IF NOT EXISTS analises (AnaliseID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, nome VARCHAR(30), PessoaID INTEGER, id_wav_data INTEGER, FOREIGN KEY (PessoaID) REFERENCES pessoas (PessoaID), FOREIGN KEY (id_wav_data) REFERENCES wav_data (id));"
        cursor.execute(sql)
        print("Tabela analises criada com sucesso!")
    except Exception as e:
        print(e)

def table_exists(conn):

    cursor = conn.cursor()

    sql = "SELECT EXISTS (SELECT name FROM sqlite_schema WHERE type='table' AND name='wav_data');"

    x = cursor.execute(sql).fetchone()

    return x 

#Configurações padrão do sistema
import json

conn = get_conn()


create_tables(conn)



#Criando configurações de entrada padrão

config_exists = select_config_input_device(conn)

if config_exists == None:
    config = {'id': 0}

    
    config = json.dumps(config)

    data = ('input_device', config)

    create_config(conn, data)



