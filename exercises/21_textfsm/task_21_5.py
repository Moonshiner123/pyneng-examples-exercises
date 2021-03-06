# -*- coding: utf-8 -*-
"""
Задание 21.5

Создать функцию send_and_parse_command_parallel.

Функция send_and_parse_command_parallel должна запускать в
параллельных потоках функцию send_and_parse_show_command из задания 21.4.

Параметры функции send_and_parse_command_parallel:
* devices - список словарей с параметрами подключения к устройствам
* command - команда
* templates_path - путь к каталогу с шаблонами TextFSM
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать словарь:
* ключи - IP-адрес устройства с которого получен вывод
* значения - список словарей (вывод который возвращает функция send_and_parse_show_command)

Пример словаря:
{'192.168.100.1': [{'address': '192.168.100.1',
                    'intf': 'Ethernet0/0',
                    'protocol': 'up',
                    'status': 'up'},
                   {'address': '192.168.200.1',
                    'intf': 'Ethernet0/1',
                    'protocol': 'up',
                    'status': 'up'}],
 '192.168.100.2': [{'address': '192.168.100.2',
                    'intf': 'Ethernet0/0',
                    'protocol': 'up',
                    'status': 'up'},
                   {'address': '10.100.23.2',
                    'intf': 'Ethernet0/1',
                    'protocol': 'up',
                    'status': 'up'}]}

Проверить работу функции на примере вывода команды sh ip int br
и устройствах из devices.yaml.
"""

import re
import yaml
from textfsm import clitable
from tabulate import tabulate
from pprint import pprint
from netmiko import ConnectHandler, NetMikoTimeoutException, NetmikoAuthenticationException
from task_21_4 import send_and_parse_show_command
import logging
from datetime import datetime
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

start_time = datetime.now()


logging.basicConfig(
    format='%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)
    
def send_and_parse_command_parallel(devices, command, templates_path, limit=3):
    final_dict = {}
    future_list = []
    device_list = []
    with ThreadPoolExecutor(max_workers=limit) as executor:
        for device in devices:
            logging.info(f'Quering {device["host"]}')
            future = executor.submit(send_and_parse_show_command, device, command, templates_path)
            future_list.append(future)
            device_list.append(device['host'])
        for d,f in zip(device_list,future_list):
            final_dict[d] = f.result()
    return final_dict

if __name__ == "__main__":
    with open("devices.yaml") as dev:
        devices = yaml.safe_load(dev)
    pprint(send_and_parse_command_parallel(devices, 'sh ip int br', 'templates'))
    print(f'Время выполнения скрипта: {datetime.now() - start_time}')
