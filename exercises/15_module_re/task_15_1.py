# -*- coding: utf-8 -*-
"""
Задание 15.1

Создать функцию get_ip_from_cfg, которая ожидает как аргумент имя файла,
в котором находится конфигурация устройства.

Функция должна обрабатывать конфигурацию и возвращать IP-адреса и маски,
которые настроены на интерфейсах, в виде списка кортежей:
* первый элемент кортежа - IP-адрес
* второй элемент кортежа - маска

Например (взяты произвольные адреса):
[('10.0.1.1', '255.255.255.0'), ('10.0.2.1', '255.255.255.0')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.


Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды,
а не ввод пользователя.

"""

import re

'''
def get_ip_from_cfg(cfg_file):
    with open(cfg_file, 'r') as f:
        ipmask_list = []
        ipmask_tuple = tuple()
        for line in f:
            match = re.search(r'ip address (?P<ip>\S+) (?P<mask>\S+)', line)
            if match:
                ip = match.group('ip')
                mask = match.group('mask')
                ipmask_tuple = (ip, mask)
                ipmask_list.append(ipmask_tuple)
    return ipmask_list

'''

regex = r'ip address (?P<ip>\S+) (?P<mask>\S+)'

def get_ip_from_cfg(cfg_file):
    with open(cfg_file, 'r') as f:
        ipmask_list=[match.groups() for match in re.finditer(regex, f.read())]
    return ipmask_list            



if __name__ == "__main__":
    print(get_ip_from_cfg('config_r1.txt'))



