# -*- coding: utf-8 -*-
"""
Задание 20.5a

Создать функцию configure_vpn, которая использует
шаблоны из задания 20.5 для настройки VPN на маршрутизаторах
на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству 1
* dst_device_params - словарь с параметрами подключения к устройству 2
* src_template - имя файла с шаблоном, который создает конфигурацию для строны 1
* dst_template - имя файла с шаблоном, который создает конфигурацию для строны 2
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов
и данных на каждом устройстве с помощью netmiko.
Функция возвращает кортеж с выводом команд с двух
маршрутизаторов (вывод, которые возвращает метод netmiko send_config_set).
Первый элемент кортежа - вывод с первого устройства (строка),
второй элемент кортежа - вывод со второго устройства.

При этом, в словаре data не указан номер интерфейса Tunnel,
который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel,
взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 5.
И надо будет настроить интерфейс Tunnel 5.

Для этого задания тест проверяет работу функции на первых двух устройствах
из файла devices.yaml. И проверяет, что в выводе есть команды настройки
интерфейсов, но при этом не проверяет настроенные номера тунелей и другие команды.
Они должны быть, но тест упрощен, чтобы было больше свободы выполнения.
"""

from netmiko import ConnectHandler, NetMikoTimeoutException
import yaml
import re
import os
from jinja2 import Environment, FileSystemLoader
#from task_20_1 import generate_config
from task_20_5 import create_vpn_config

data = {}

def send_show_command(device, command):
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
        prompt = ssh.find_prompt()
    return f"{prompt}{command}\n{result}\n"
    
    
def send_cfg_commands(device, commands):
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        result = ssh.send_config_set(commands)
    return f"{result}\n"


def configure_vpn(src_device_params, dst_device_params, src_template, dst_template, vpn_data_dict):
    '''
    Extracting list of all configured tun_id's on both ends
    '''
    print("Extracting list of all configured tun_id's on both ends")
    regex = r'Tunnel(?P<tun_id>\d+)'
    show1_tun_id_list = []
    show2_tun_id_list = []
    show1 = send_show_command(src_device_params, "sh ip int b")
    show2 = send_show_command(dst_device_params, "sh ip int b")
    match1 = re.finditer(regex, show1)
    match2 = re.finditer(regex, show2)
    show1_tun_id_list = [int(m.group("tun_id")) for m in match1]
    show2_tun_id_list = [int(n.group("tun_id")) for n in match2]
    tun_id_set = set(show1_tun_id_list) | set(show2_tun_id_list)
    '''
    Finding out which tun_id is free
    '''
    print('Finding out which tun_id is free')
    tun_id_list = list(tun_id_set)
    max_id = tun_id_list[-1] + 2
    for i in range(max_id):
        if  not i in tun_id_list:
            tunnel_id = i
            break
    '''
    Generating configs
    ''' 
    print('Generating configs')
    vpn_data_dict["tun_num"] = tunnel_id
    config1, config2 = create_vpn_config(src_template, dst_template, vpn_data_dict)
   
    '''
    Applying config
    '''
    print('Applying configs')
    applied_config_1 = send_cfg_commands(src_device_params, config1.split("\n"))
    applied_config_2 = send_cfg_commands(dst_device_params, config2.split("\n"))
    return applied_config_1, applied_config_2
    

    

if __name__ == "__main__":
    data = {
    "tun_num": None,
    "wan_ip_1": "192.168.100.1",
    "wan_ip_2": "192.168.100.2",
    "tun_ip_1": "10.0.1.1 255.255.255.252",
    "tun_ip_2": "10.0.1.2 255.255.255.252"}
    
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    #src_device_params = devices[0]
    #dst_device_params = devices[1]
    #data_file = "data_files/gre_ipsec_vpn.yml"
    template1 = "templates/gre_ipsec_vpn_1.txt"
    template2 = "templates/gre_ipsec_vpn_2.txt"
    result1, result2 = configure_vpn(devices[0], devices[1], template1, template2, data)
    print(result1)
    print(result2)
    
