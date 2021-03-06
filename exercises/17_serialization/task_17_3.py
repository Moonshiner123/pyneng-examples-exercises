# -*- coding: utf-8 -*-
"""
Задание 17.3

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
"""

import glob
import re
from pprint import pprint


def parse_sh_cdp_neighbors(input_string):
    cdp_dict = {}
    ldevice = re.search(r'(?P<ldevice>\S+)[>#]', input_string).group('ldevice')
    cdp_dict[ldevice] = {}
    
    regex = (r'(?P<rdevice>\S+) +(?P<lintf>\S+ \d+/\d+) .*?(?P<rintf>\S+ \d+/\d+)')
    match = re.finditer(regex, input_string)
    for m in match:
        cdp_dict[ldevice][m.group('lintf')] = {m.group('rdevice'): m.group('rintf')}
    return cdp_dict
    
if __name__ == "__main__":
    test_input_string = open('sh_cdp_n_sw1.txt').read()
    print(parse_sh_cdp_neighbors(test_input_string))
