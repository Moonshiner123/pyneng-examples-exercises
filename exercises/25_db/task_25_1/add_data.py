import yaml
import sqlite3
import re
import create_db as db_init

db_filename = 'dhcp_snooping.db'
switches_addresses = 'switches.yml'

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
    #Получаем хостнейм из имени файла
    sw_regex = r'(\S+)_dhcp_snooping.txt'
    sw_name = re.match(sw_regex,dhcp_snoop_filename)
    switch = sw_name.group(1)
    #print('Получаем хостнейм из имени файла: ', switch)
    #Парсим файл и получаем список кортежей
    regex = re.compile(r'(?P<mac>\S+) +(?P<ip>\S+) +\d+ +\S+ +(?P<vlan>\d+) +(?P<intf>\S+)')
    result = []
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
    with open(yml_file) as f:
        templates = yaml.safe_load(f)
    #print (templates)
    #print(templates.values())
    sw_list = []
    for equipment in templates.values():
        #print(equipment)
        for hostname, address in equipment.items():
            #print(hostname, address)
            sw_list.append((hostname, address))
    return sw_list


if __name__ == "__main__":
    conn = db_init.create_connection(db_filename)
    #Добавление данных в БД, таблица "switches"
    print('Добавляю данные в таблицу switches...')
    data_switches = parse_yaml_file(switches_addresses)
    query_switches = '''insert into switches (hostname, location) values (?, ?)'''
    write_rows_to_db(conn, query_switches, data_switches)
    
    #Добавление данных в БД, таблица "dhcp"
    print('Добавляю данные в таблицу dhcp...')
    query_dhcp = '''insert into dhcp (mac, ip, vlan, interface, switch) values (?, ?, ?, ?, ?)'''
    files = ['sw1_dhcp_snooping.txt', 'sw2_dhcp_snooping.txt', 'sw3_dhcp_snooping.txt']
    for filename in files:
        data_dhcp = parse_dhcp_snooping_output(filename)
        write_rows_to_db(conn, query_dhcp, data_dhcp)
        
    
    
