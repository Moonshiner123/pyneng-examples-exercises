# -*- coding: utf-8 -*-
"""
Задание 7.3a

Сделать копию скрипта задания 7.3.

Переделать скрипт:  Отсортировать вывод по номеру VLAN

В результате должен получиться такой вывод:
10       01ab.c5d0.70d0      Gi0/8
10       0a1b.1c80.7000      Gi0/4
100      01bb.c580.7000      Gi0/1
200      0a4b.c380.7c00      Gi0/2
200      1a4b.c580.7000      Gi0/6
300      0a1b.5c80.70f0      Gi0/7
300      a2ab.c5a0.700e      Gi0/3
500      02b1.3c80.7b00      Gi0/5
1000     0a4b.c380.7d00      Gi0/9

Обратите внимание на vlan 1000 - он должен выводиться последним.
Правильной сортировки можно добиться, если vlan будет числом, а не строкой.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
dictionary={}

with open(f"CAM_table.txt", "r") as file:
    for line in file:
        line=line.split()
        if line and line[0][0].isdigit():
            vlan=int(line[0])
            mac=line[1]
            port=line[3]
            dictionary[vlan]={}
            dictionary[vlan]['mac']=mac
            dictionary[vlan]['port']=port

sorted_dictionary_list=sorted(dictionary)
#print(dictionary)
#print(sorted_dictionary_list)

for i in sorted_dictionary_list:
    #Fuck! Have to play with those damn single and double quotes for a while!
    #Behavior differs with and without f-string.
    #print(i)
    #print(dictionary[i]['mac'])
    #print(dictionary[i]['port'])
    print(f'{i:<10} {dictionary[i]["mac"]:<20}  {dictionary[i]["port"]}')

