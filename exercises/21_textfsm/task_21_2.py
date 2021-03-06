# -*- coding: utf-8 -*-
"""
Задание 21.2

Сделать шаблон TextFSM для обработки вывода sh ip dhcp snooping binding
и записать его в файл templates/sh_ip_dhcp_snooping.template

Вывод команды находится в файле output/sh_ip_dhcp_snooping.txt.

Шаблон должен обрабатывать и возвращать значения таких столбцов:
* mac - такого вида 00:04:A3:3E:5B:69
* ip - такого вида 10.1.10.6
* vlan - 10
* intf - FastEthernet0/10

Проверить работу шаблона с помощью функции parse_command_output из задания 21.1.
"""


from tabulate import tabulate
from task_21_1 import parse_command_output
import re


if __name__ == "__main__":
    regex = r'(\S+) +(\S+) +\S+ +\S+ +(\d+) +(\S+)'
    regex1 = r'(\S+) +(\S+) +\S+ +\S+ +(\d+) +(\S+)'
    output = "output/sh_ip_dhcp_snooping.txt"
    template = "templates/sh_ip_dhcp_snooping.template"
    with open(output) as f, open(template) as t:
        #match = re.finditer(regex1, f.read())
        #list1 = [m.groups() for m in match]
        #print(list1)
        #print(f.read())
        result = parse_command_output("templates/sh_ip_dhcp_snooping.template", f.read())
    print(result)
    print(tabulate(result))

