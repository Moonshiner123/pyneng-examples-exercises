import yaml
import sqlite3
import re
import os
from pprint import pprint
from datetime import timedelta, datetime
from tabulate import tabulate



def create_db(db_filename, schema_filename):
    '''
    Функция создает файл БД db_filename и таблицы в этом файле в сответствии с файлом
    schema_name
    '''
    db_exists = os.path.exists(db_filename)
    if not db_exists:
        connection = sqlite3.connect(db_filename)
        print('Создаю базу данных...')
        with open(schema_filename, 'r') as f:
            schema = f.read()
        connection.executescript(schema)
    else:
        print('База данных уже существует')
    
#sqlite3 dhcp_snooping.db "SELECT name FROM sqlite_master WHERE type='table'"



def write_rows_to_db(connection, query, data):
    '''
    Функция ожидает аргументы:
     * connection - соединение с БД
     * query - запрос, который нужно выполнить
     * data - данные, которые надо передать в виде списка кортежей

    Функция пытается записать поочереди кортежи из списка data.
    Если кортеж удалось записать успешно, изменения сохраняются в БД.
    Если в процессе записи кортежа возникла ошибка, транзакция откатывается.

    Флаг verbose контролирует то, будут ли выведены сообщения об удачной
    или неудачной записи кортежа.
    '''
    for row in data:
        try:
            with connection:
                connection.execute(query, row)
        except sqlite3.IntegrityError as e:
            print("При добавлении данных: ('{}') Возникла ошибка: {}".format(', '.join(row), e))
            

def parse_dhcp_snooping_output(dhcp_snoop_filename):
    '''
    Функция парсит содержимое файла с выводом "sh ip dhcp snooping" и выдает список с кортежами
    вида (mac, ip, vlan, intf, switch)
    '''
    print(dhcp_snoop_filename)
    sw_regex = r'(\S+)_dhcp_snooping.txt'
    sw_name = re.match(sw_regex,dhcp_snoop_filename)
    switch = sw_name.group(1)
    regex = re.compile(r'(?P<mac>\S+) +(?P<ip>\S+) +\d+ +\S+ +(?P<vlan>\d+) +(?P<intf>\S+)')
    result = []
    #Парсим файл и получаем список кортежей
    with open(dhcp_snoop_filename) as data:
        for line in data:
            match = regex.search(line)
            if match:
                result.append((match.group('mac'), match.group('ip'), match.group('vlan'), match.group('intf'), switch))
    return result


def parse_yaml_file(yml_file):
    '''
    Функция парсит содержимое yaml-файла с адресами железок и выдает список с кортежами
    вида (hostname, address)
    '''
    for filename in yml_file:
        with open(filename) as f:
            templates = yaml.safe_load(f)
        sw_list = []
        for equipment in templates.values():
            for hostname, address in equipment.items():
                sw_list.append((hostname, address))
    return sw_list

def parse_dhcp_snooping_filenames(user_input):
    '''
    Функция делает список имен файлов из пользовательского ввода типа 
    sw[1-3]_dhcp_snooping.txt
    '''
    user_input_regex = r'(?P<letters_part>\S+?)(?P<numbers_part>\[\d+-\d+\])?_dhcp_snooping.txt'
    sw_name = re.search(user_input_regex,str(user_input))
    #print(sw_name.group('letters_part'))
    #print(sw_name.group('numbers_part'))
    if not sw_name.group('numbers_part'):
        result = [sw_name.group('letters_part') + '_dhcp_snooping.txt']
    else:
        numbers_part = sw_name.group('numbers_part')
        numbers_part_regex = r'\[(?P<number_1>\d+)-(?P<number_2>\d+)\]'
        numbers = re.search(numbers_part_regex, numbers_part)
        number_1 = int(numbers.group('number_1'))
        number_2 = int(numbers.group('number_2')) + 1
        result = [sw_name.group('letters_part') + str(number) + '_dhcp_snooping.txt' for number in range(number_1, number_2)]
    return result
        
    

def add_data_switches(db_filename, sw_filename):
    '''
    Функция добавляет в БД данные из обработанного файла с адресами коммутаторов
    '''
    data_switches = parse_yaml_file(sw_filename)
    query_switches = "insert into switches (hostname, location) values (?, ?)"
    connection = sqlite3.connect(db_filename)
    write_rows_to_db(connection, query_switches, data_switches)
    


def add_data(db_filename, input_files):
    #files = ['sw1_dhcp_snooping.txt', 'sw2_dhcp_snooping.txt', 'sw3_dhcp_snooping.txt']
    '''
    Проходим по списку файлов.
    '''
    print(input_files)
    connection = sqlite3.connect(db_filename)
    #input_files_list = parse_dhcp_snooping_filenames(input_files)
    for filename in input_files:
        data_dhcp = parse_dhcp_snooping_output(filename)
        '''
        Получили список кортежей вида (mac, ip, vlan, intf, switch) с устройства, сейчас будем обрабатывать кортежи по одному.
        '''
        for row in data_dhcp:
            '''
            Распаковка значений из кортежа.
            '''
            mac, ip, vlan, interface, switch = row
            '''
            Поиск строки в БД с таким же маком, получаем список из одного кортежа.
            '''
            db_select_where_query = "SELECT * from dhcp where mac = '{}'".format(mac)
            db_entry = connection.execute(db_select_where_query).fetchall()
            active_flag = 1
            if db_entry:
                '''
                Если строка в БД с таким же маком найдена, достаем кортеж из списка и распаковываем его.
                '''
                for entry in db_entry:
                    curr_mac, curr_ip, curr_vlan, curr_interface, curr_switch, _, _ = entry
                curr_row = (curr_mac, curr_ip, curr_vlan, curr_interface, curr_switch)
                print('Существующая строка из БД с тем же маком:\n', curr_row)
                '''
                Сравниваем значения из выводов sh ip dhcp snooping и содержимого sql таблицы для текущего мака (без учета флага active).
                '''
                if row == curr_row:
                    print('Точно такая же строка уже есть, добавляю 1  в active')
                    update_query = "UPDATE dhcp set active = ?, last_active = datetime() WHERE mac = '{}'".format(mac)
                    curr_row = (active_flag,)
                    write_rows_to_db(connection, update_query, [curr_row,])
                    #connection.execute("UPDATE dhcp set active = 1 WHERE mac = '{}'".format(mac))
                    #pprint(connection.execute("SELECT * from dhcp").fetchall())
                else:
                    #active_flag = 1
                    print('MAC перепрыгнул на другой порт, перезаписываю данные')
                    replace_query = '''REPLACE INTO dhcp  values (?, ?, ?, ?, ?, ?, datetime())'''
                    curr_row = (mac, ip, vlan, interface, switch, active_flag)
                    write_rows_to_db(connection, replace_query, [curr_row,])
                    #connection.execute(f"REPLACE INTO dhcp  values ('{mac}', '{ip}', '{vlan}', '{interface}', '{switch}', '{active_flag}')")
                    #pprint(connection.execute("SELECT * from dhcp").fetchall())
            else:
                '''
                Если строка в БД с таким же маком не найдена, делаем новую запись в БД.
                '''
                print('Оппачки! Такого мака еще не было! Создаю новую запись')
                insert_query_dhcp = '''insert into dhcp (mac, ip, vlan, interface, switch, active, last_active) values (?, ?, ?, ?, ?, ?, datetime())'''
                curr_row = (mac, ip, vlan, interface, switch, active_flag)
                write_rows_to_db(connection, insert_query_dhcp, [curr_row,])
                #pprint(connection.execute("SELECT * from dhcp").fetchall())

    '''
    Удаление устаревших записей
    '''
    #os.chdir('/home/python/repos/pyneng-examples-exercises/exercises/25_db/task_25_5a/')
    now = datetime.today().replace(microsecond=0)
    week_ago = now - timedelta(days=7)
    week_ago = str(week_ago)
    print(week_ago)
    db_select_where_query = f"select * from dhcp where last_active < '{week_ago}'"
    print(db_select_where_query)
    pprint(connection.execute(db_select_where_query).fetchall(), width = 150)
    db_delete_where_query = f"DELETE from dhcp where last_active < '{week_ago}'"
    #write_rows_to_db(connection, db_delete_where_query, [])
        
    connection.execute(db_delete_where_query)
    pprint(connection.execute("SELECT * from dhcp").fetchall(), width = 150)
    connection.commit()
    
def get_data(db_filename, key, value):
    connection = sqlite3.connect(db_filename)
    keys = ['mac', 'ip', 'vlan', 'interface', 'switch', 'active', 'last_active']
    query = "select * from dhcp where {} = ?".format(key)
    result = connection.execute(query, (value, ))
    print(tabulate(result, headers = keys))  
    
def get_all_data(db_filename):
    connection = sqlite3.connect(db_filename)
    keys = ['mac', 'ip', 'vlan', 'interface', 'switch', 'active', 'last_active']
    query = "select * from dhcp"
    result = connection.execute(query)
    print(tabulate(result, headers = keys)) 
