# -*- coding: utf-8 -*-
"""
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Переделать скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Пример работы скрипта:

Enter VLAN number: 10
10       0a1b.1c80.7000      Gi0/4
10       01ab.c5d0.70d0      Gi0/8

Ограничение: Все задания надо выполнять используя только пройденные темы.

""" 

vlan=int(input("Введите номер VLAN: "))

'''
listoflists=[]

with open(f"CAM_table.txt", "r") as file:
    for line in file:
        line=line.split()
        if line and line[0][0].isdigit():
            sublist=[int(line[0]), line[1], line[3]]
            listoflists.append(sublist)
            
sorted_list=sorted(listoflists)
reverse_sorted_list=sorted_list[::-1]


for i in reverse_sorted_list:
    if vlan in i:
        print(f'{i[0]:<10} {i[1]:<20} {i[2]}')

'''

with open(f"CAM_table.txt", "r") as file:
    for line in file:
        line=line.split()
        if line and line[0].isdigit() and int(line[0])==vlan:
            print(f'{line[0]:10} {line[1]:20} {line[3]:10}')
