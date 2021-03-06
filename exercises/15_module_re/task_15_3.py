# -*- coding: utf-8 -*-
"""
Задание 15.3

Создать функцию convert_ios_nat_to_asa, которая конвертирует правила NAT
из синтаксиса cisco IOS в cisco ASA.

Функция ожидает такие аргументы:
- имя файла, в котором находится правила NAT Cisco IOS
- имя файла, в который надо записать полученные правила NAT для ASA

Функция ничего не возвращает.

Проверить функцию на файле cisco_nat_config.txt.

Пример правил NAT cisco IOS
ip nat inside source static tcp 10.1.2.84 22 interface GigabitEthernet0/1 20022
ip nat inside source static tcp 10.1.9.5 22 interface GigabitEthernet0/1 20023

И соответствующие правила NAT для ASA:
object network LOCAL_10.1.2.84
 host 10.1.2.84
 nat (inside,outside) static interface service tcp 22 20022
object network LOCAL_10.1.9.5
 host 10.1.9.5
 nat (inside,outside) static interface service tcp 22 20023

В файле с правилами для ASA:
- не должно быть пустых строк между правилами
- перед строками "object network" не должны быть пробелы
- перед остальными строками должен быть один пробел

Во всех правилах для ASA интерфейсы будут одинаковыми (inside,outside).
"""


import re

regex = (r'ip nat inside source static (?P<proto>\w+) '
         r'(?P<inside_ip>\S+) (?P<inside_port>\d+) '
         r'interface GigabitEthernet0/1 (?P<outside_port>\d+)')
        

def convert_ios_nat_to_asa(ios,asa):
    with open(ios) as src, open(asa, 'w') as dest:
        for line in src:
            asa_string = re.search(regex,line)
            print(f'object network LOCAL_{asa_string.group("inside_ip")}', file=dest)
            print(f' host {asa_string.group("inside_ip")}', file=dest)
            print(f' nat (inside,outside) static interface service {asa_string.group("proto")} {asa_string.group("inside_port")} {asa_string.group("outside_port")}', file=dest)

                
if __name__ == "__main__":
    convert_ios_nat_to_asa('cisco_nat_config.txt', 'cisco_asa_config.txt')
