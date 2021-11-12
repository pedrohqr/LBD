from configparser import ConfigParser
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

#lê o arquivo .ini de configurações
def config(filename='database_config.ini', section='postgresql'):
    # criar parser
    parser = ConfigParser()
    # ler configurações
    parser.read(filename)

    # ler sessões
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

#cria o banco de dados em runtime
def create_dataBase():
    try:
        print('Criando banco de dados...')
        con = psycopg2.connect(host=config(section='postgresql')["host"],
                               port=config(section='postgresql')["port"],
                               user=config(section='postgresql')["user"],
                               password=config(section='postgresql')["password"])

        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        cursor = con.cursor()

        name_Database = config(section='postgresql')["dbname"]

        sqlCreateDatabase = "CREATE DATABASE "+name_Database+";"

        cursor.execute(sqlCreateDatabase)

        con.commit()
        cursor.close()
        con.close()

        print(cursor.statusmessage)
    except Exception as erro:
        print(erro)

def set_Script():
    try:
        print('Inserindo script...')
        parametros=config()
        con = psycopg2.connect(**parametros)
        cursor=con.cursor()
        cursor.execute(open("script_db.sql", "r").read())

        con.commit()
        cursor.close()
        con.close()

        print(cursor.statusmessage)
        print('Banco criado com sucesso!')
        print('\n')
    except Exception as erro:
        print(erro)