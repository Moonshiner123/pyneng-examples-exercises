import os
import sqlite3


db_filename = 'dhcp_snooping.db'
schema_filename = 'dhcp_snooping_schema.sql'
db_exists = os.path.exists(db_filename)


def create_connection(db_name):
    '''
    Функция создает соединение с БД db_name,
    создает таблицы в сответствии с файлом
    schema_name и возвращает соединение
    '''
    connection = sqlite3.connect(db_name)
    return connection
    
    
 
def create_schema(schema_name,connection_name):
    '''
    Функция создает таблицы в сответствии с файлом
    schema_name
    '''
    with open(schema_name, 'r') as f:
        schema = f.read()
    connection_name.executescript(schema)
  



if __name__ == "__main__":
    if not db_exists:
        print('Создаю базу данных...')
        conn = create_connection(db_filename)
        create_schema(schema_filename,conn)
    else:
        print('База данных существует')
        
