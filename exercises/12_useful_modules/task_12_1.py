# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

import subprocess


def ping_ip_addresses(ip_list):
    reachable_ip_list=[]
    unreachable_ip_list=[]
    for ip in ip_list:
        reply = subprocess.run(f'ping -c 3 -n {ip}' , shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if reply.returncode == 0:
            reachable_ip_list.append(ip)
        else:
            unreachable_ip_list.append(ip)
    return reachable_ip_list, unreachable_ip_list
    

if __name__ == "__main__":
    print(ping_ip_addresses(['8.8.8.8', '192.168.8.1', 'a', '8.8.4.4', '172.28.9.4']))

            
