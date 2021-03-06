# -*- coding: utf-8 -*-
"""
Задание 12.2


Функция ping_ip_addresses из задания 12.1 принимает только список адресов,
но было бы удобно иметь возможность указывать адреса с помощью диапазона,
например, 192.168.100.1-10.

В этом задании необходимо создать функцию convert_ranges_to_ip_list,
которая конвертирует список IP-адресов в разных форматах в список,
где каждый IP-адрес указан отдельно.

Функция ожидает как аргумент список, в котором содержатся IP-адреса
и/или диапазоны IP-адресов.

Элементы списка могут быть в формате:
* 10.1.1.1
* 10.1.1.1-10.1.1.10
* 10.1.1.1-10

Если адрес указан в виде диапазона, надо развернуть диапазон в отдельные
адреса, включая последний адрес диапазона.
Для упрощения задачи, можно считать, что в диапазоне всегда меняется только
последний октет адреса.

Функция возвращает список IP-адресов.

Например, если передать функции convert_ranges_to_ip_list такой список:
['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']

Функция должна вернуть такой список:
['8.8.4.4', '1.1.1.1', '1.1.1.2', '1.1.1.3', '172.21.41.128',
 '172.21.41.129', '172.21.41.130', '172.21.41.131', '172.21.41.132']

"""

import ipaddress

def check_if_ip_is_address(ip_address):
    try:
        ipaddress.ip_address(ip_address)
        return True
    except ValueError:
        return False

def convert_ranges_to_ip_list(ip_ranges):
    expanded_range=[]
    for ip in ip_ranges:
        if check_if_ip_is_address(ip):
            expanded_range.append(ip)
        elif not check_if_ip_is_address(ip) and len(ip.split('-')[-1]) <= 3:
            ip1=ip.split('-')[0]
            diff = int(ip.split('-')[-1]) - int(ip1.split('.')[-1])
            for i in range(diff+1):
                ip1=ipaddress.ip_address(ip1)
                expanded_range.append(str(ip1))
                ip1+=1
        elif not check_if_ip_is_address(ip) and check_if_ip_is_address(ip.split('-')[-1]):
            ip1=ip.split('-')[0]
            ip2=ip.split('-')[1]
            diff = int(ip2.split('.')[-1]) - int(ip1.split('.')[-1])
            for i in range(diff+1):
                ip1=ipaddress.ip_address(ip1)
                expanded_range.append(str(ip1))
                ip1+=1
    return expanded_range
    
    
if __name__ == "__main__":
    print(convert_ranges_to_ip_list(['8.8.4.4', '1.1.1.1-3', '172.21.41.128-172.21.41.132']))
                
                
                
                
                
                
                
