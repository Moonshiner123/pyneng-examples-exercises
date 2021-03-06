# -*- coding: utf-8 -*-
"""
Задание 21.4

Создать функцию send_and_parse_show_command.

Параметры функции:
* device_dict - словарь с параметрами подключения к одному устройству
* command - команда, которую надо выполнить
* templates_path - путь к каталогу с шаблонами TextFSM
* index - имя индекс файла, значение по умолчанию "index"

Функция должна подключаться к одному устройству, отправлять команду show
с помощью netmiko, а затем парсить вывод команды с помощью TextFSM.

Функция должна возвращать список словарей с результатами обработки
вывода команды (как в задании 21.1a):
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на примере вывода команды sh ip int br
и устройствах из devices.yaml.
"""


import re
import yaml
from textfsm import clitable
from tabulate import tabulate
from pprint import pprint
from netmiko import ConnectHandler, NetMikoTimeoutException


def send_and_parse_show_command(device_dict, command, templates_path, index="index"):
    result = []
    with ConnectHandler(**device_dict) as ssh:
        ssh.enable()
        command_output = ssh.send_command(command)
        
    cli_table = clitable.CliTable(index, templates_path)
    attributes = {'Command': command, 'Vendor': 'cisco_ios'}
    cli_table.ParseCmd(command_output, attributes)
    header = list(cli_table.header)
    data_rows = [list(row) for row in cli_table]
    result = [dict(zip(header, row)) for row in data_rows]
    return result

if __name__ == "__main__":
    with open("devices.yaml") as dev:
        devices = yaml.safe_load(dev)
    for device in devices:
        pprint(send_and_parse_show_command(device, 'sh ip int br', 'templates'))
        print(tabulate(send_and_parse_show_command(device, 'sh ip int br', 'templates')))
