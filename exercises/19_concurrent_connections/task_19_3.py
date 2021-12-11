# -*- coding: utf-8 -*-
"""
Задание 19.3

Создать функцию send_command_to_devices, которая отправляет разные
команды show на разные устройства в параллельных потоках, а затем записывает
вывод команд в файл. Вывод с устройств в файле может быть в любом порядке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* commands_dict - словарь в котором указано на какое устройство отправлять
  какую команду. Пример словаря - commands
* filename - имя файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в файл в таком формате (перед выводом
команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh int desc
Interface                      Status         Protocol Description
Et0/0                          up             up
Et0/1                          up             up
Et0/2                          admin down     down
Et0/3                          admin down     down
Lo9                            up             up
Lo19                           up             up
R3#sh run | s ^router ospf
router ospf 1
 network 0.0.0.0 255.255.255.255 area 0


Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml и словаре commands
"""

# Этот словарь нужен только для проверки работа кода, в нем можно менять IP-адреса
# тест берет адреса из файла devices.yaml
commands = {
    "192.168.100.3": "sh run | s ^router ospf",
    "192.168.100.1": "sh ip int br",
    "192.168.100.2": "sh int desc",
}

from pprint import pprint
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
from datetime import datetime
import time
import yaml
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
start_time = datetime.now()



logging.basicConfig(
    format='%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)
    

def send_show(command, device):
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            output = ssh.find_prompt() + ssh.send_command(command, strip_command=False) + '\n'
        return output
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)
        
        
def send_command_to_devices(devices, commands_dict, filename, limit=3):

    logging.info(f'Sending commands to devices from your list, please wait...')
    logging.info(f'Using {limit} workers')
    with open(filename, "w") as destination_file:
        with ThreadPoolExecutor(max_workers=limit) as executor:
            future_list = []
            for device in devices:
                logging.info(f'Quering {device["host"]}')
                future = executor.submit(send_show, commands_dict[device["host"]], device)
                future_list.append(future)
            for f in as_completed(future_list):
                #print(f.result())
                logging.info(f'Writing to file: {f.result()}')
                destination_file.write(f.result())
            
        

if __name__ == "__main__":
    with open("devices.yaml") as dev:
        devices = yaml.safe_load(dev)
    send_command_to_devices(devices, commands, "my_test_file_19.3")
    print(f'Время выполнения скрипта: {datetime.now() - start_time}')

