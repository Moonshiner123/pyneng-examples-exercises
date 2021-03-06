# -*- coding: utf-8 -*-
"""
Задание 21.3

Создать функцию parse_command_dynamic.

Параметры функции:
* command_output - вывод команды (строка)
* attributes_dict - словарь атрибутов, в котором находятся такие пары ключ-значение:
 * 'Command': команда
 * 'Vendor': вендор
* index_file - имя файла, где хранится соответствие между командами и шаблонами.
  Значение по умолчанию - "index"
* templ_path - каталог, где хранятся шаблоны. Значение по умолчанию - "templates"

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br.
"""


import re
from textfsm import clitable
from tabulate import tabulate
from pprint import pprint



def parse_command_dynamic(command_output, attributes_dict, index_file='index', templ_path='templates'):
    result = []
    cli_table = clitable.CliTable(index_file, templ_path)
    cli_table.ParseCmd(command_output, attributes_dict)
    header = list(cli_table.header)
    data_rows = [list(row) for row in cli_table]
    for row in data_rows:
        dict_element = dict(zip(header, row))
        result.append(dict_element)
    return result

if __name__ == "__main__":
    output = 'output/sh_ip_int_br.txt'
    
    with open(output) as f:
        out=f.read()
        regex = r'\S+[#>](?P<command>.+)\n'
        match = re.search(regex, out)
        command = match.group('command')
        #print(command)
        attributes = {'Command': command, 'Vendor': 'cisco_ios'}
        pprint(parse_command_dynamic(out, attributes))
        print(tabulate(parse_command_dynamic(out, attributes)))

