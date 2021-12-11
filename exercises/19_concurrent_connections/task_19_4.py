# -*- coding: utf-8 -*-
"""
Задание 19.4

Создать функцию send_commands_to_devices, которая отправляет команду show или config
на разные устройства в параллельных потоках, а затем записывает вывод команд в файл.

Параметры функции:
* devices - список словарей с параметрами подключения к устройствам
* filename - имя файла, в который будут записаны выводы всех команд
* show - команда show, которую нужно отправить (по умолчанию, значение None)
* config - команды конфигурационного режима, которые нужно отправить (по умолчанию None)
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция ничего не возвращает.

Аргументы show, config и limit должны передаваться только как ключевые. При передачи
этих аргументов как позиционных, должно генерироваться исключение TypeError.

In [4]: send_commands_to_devices(devices, 'result.txt', 'sh clock')
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-4-75adcfb4a005> in <module>
----> 1 send_commands_to_devices(devices, 'result.txt', 'sh clock')

TypeError: send_commands_to_devices() takes 2 positional argument but 3 were given


При вызове функции send_commands_to_devices, всегда должен передаваться
только один из аргументов show, config. Если передаются оба аргумента, должно
генерироваться исключение ValueError.


Вывод команд должен быть записан в файл в таком формате
(перед выводом команды надо написать имя хоста и саму команду):

R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.1   YES NVRAM  up                    up
Ethernet0/1                192.168.200.1   YES NVRAM  up                    up
R2#sh arp
Protocol  Address          Age (min)  Hardware Addr   Type   Interface
Internet  192.168.100.1          76   aabb.cc00.6500  ARPA   Ethernet0/0
Internet  192.168.100.2           -   aabb.cc00.6600  ARPA   Ethernet0/0
Internet  192.168.100.3         173   aabb.cc00.6700  ARPA   Ethernet0/0
R3#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
Ethernet0/0                192.168.100.3   YES NVRAM  up                    up
Ethernet0/1                unassigned      YES NVRAM  administratively down down

Пример вызова функции:
In [5]: send_commands_to_devices(devices, 'result.txt', show='sh clock')

In [6]: cat result.txt
R1#sh clock
*04:56:34.668 UTC Sat Mar 23 2019
R2#sh clock
*04:56:34.687 UTC Sat Mar 23 2019
R3#sh clock
*04:56:40.354 UTC Sat Mar 23 2019

In [11]: send_commands_to_devices(devices, 'result.txt', config='logging 10.5.5.5')

In [12]: cat result.txt
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 10.5.5.5
R1(config)#end
R1#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#logging 10.5.5.5
R2(config)#end
R2#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#logging 10.5.5.5
R3(config)#end
R3#

In [13]: commands = ['router ospf 55', 'network 0.0.0.0 255.255.255.255 area 0']

In [13]: send_commands_to_devices(devices, 'result.txt', config=commands)

In [14]: cat result.txt
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#router ospf 55
R1(config-router)#network 0.0.0.0 255.255.255.255 area 0
R1(config-router)#end
R1#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#router ospf 55
R2(config-router)#network 0.0.0.0 255.255.255.255 area 0
R2(config-router)#end
R2#
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R3(config)#router ospf 55
R3(config-router)#network 0.0.0.0 255.255.255.255 area 0
R3(config-router)#end
R3#


Для выполнения задания можно создавать любые дополнительные функции.
"""


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
    

def send_show(command_list, device):
    show_output_list = []
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            prompt = ssh.find_prompt()
            for command in command_list:
                output = ssh.send_command(command, strip_command=False) 
                result = prompt + output + '\n'
                show_output_list.append(result)
        return show_output_list
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)


def send_config(command_list, device):
    conf_output_list = []
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            prompt = ssh.find_prompt()
            for command in command_list:
                output = ssh.send_config_set(command, strip_command=False) 
                result = prompt + output + '\n'
                conf_output_list.append(result)
        return conf_output_list
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)
        
        
def send_commands_to_devices(devices, filename, *, show=None, config=None, limit=3):
    with open(filename, "w") as destination_file:
        logging.info(f'Sending commands to devices from your list, please wait...')
        logging.info(f'Using {limit} workers')
        
        if show and  config:
            raise ValueError('Функция работает только с одним типом команд (show/config)')
        elif show:
            function = send_show
            commands = show
        elif config:
            function = send_config
            commands = config
            
        if type(commands) == str:
            commands = [commands]
            
        with ThreadPoolExecutor(max_workers=limit) as executor:
                future_list = []
                for device in devices:
                    logging.info(f'Quering {device["host"]}')
                    future = executor.submit(function, commands, device)
                    future_list.append(future)
                for f in as_completed(future_list):
                    #print(f.result())
                    logging.info(f'Writing to file: {f.result()}')
                    destination_file.write("".join(f.result()))
        
            
            
        

if __name__ == "__main__":
    with open("devices.yaml") as dev:
        devices = yaml.safe_load(dev)
    send_commands_to_devices(devices, "my_test_file_19.4", show=["show ver", "sh clock"])
    print(f'Время выполнения скрипта: {datetime.now() - start_time}')
