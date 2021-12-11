# -*- coding: utf-8 -*-
"""
Задание 19.2

Создать функцию send_show_command_to_devices, которая отправляет одну и ту же
команду show на разные устройства в параллельных потоках, а затем записывает
вывод команд в файл. Вывод с устройств в файле может быть в любом порядке.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* command - команда
* filename - имя текстового файла, в который будут записаны выводы всех команд
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Вывод команд должен быть записан в обычный текстовый файл в таком формате
(перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.2   YES NVRAM  up                    up
Ethernet0/1                10.1.1.1        YES NVRAM  administratively down down
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Для выполнения задания можно создавать любые дополнительные функции.

Проверить работу функции на устройствах из файла devices.yaml
"""



import subprocess
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
            prompt = ssh.find_prompt()
            output = prompt + ssh.send_command(command, strip_command=False) + '\n'
        return output
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)
        
        
def send_show_command_to_devices(devices, command, filename, limit=3):

    logging.info(f'Sending {command} command to devices from your list, please wait...')
    logging.info(f'Using {limit} workers')
    with open(filename, "w") as destination_file:
        with ThreadPoolExecutor(max_workers=limit) as executor:
            future_list = []
            for device in devices:
                logging.info(f'Quering {device["host"]}')
                future = executor.submit(send_show, command, device)
                future_list.append(future)
            for f in as_completed(future_list):
                #print(f.result())
                logging.info(f'Writing to file: {f.result()}')
                destination_file.write(f.result())
            
        

if __name__ == "__main__":
    with open("devices.yaml") as dev:
        devices = yaml.safe_load(dev)
    send_show_command_to_devices(devices, "sh ip int b", "my_test_file")
    print(f'Время выполнения скрипта: {datetime.now() - start_time}')


