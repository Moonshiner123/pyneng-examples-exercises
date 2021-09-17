# -*- coding: utf-8 -*-
"""
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт: Если адрес был введен неправильно, запросить адрес снова.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

ip_correct=False

while not ip_correct:
    ip=input("Введите IP-адрес (например, 10.1.1.1): ")
    ip_list=ip.split(".")
    if len(ip_list)==4:
        for octet in ip_list:
            if octet.isdigit() and int(octet)<256:
                continue
            else:
                print("Неправильный IP-адрес1")
                ip_correct=False
                break
        else:
            ip_correct=True
            first_octet=int(ip[:ip.find(".")])
            if 1<=first_octet<=223:
                print("unicast")
            elif 224<=first_octet<=239:
                print("multicast")
            elif ip=="255.255.255.255":
                print("local broadcast")
            elif ip=="0.0.0.0":
                print("unassigned")
            else:
                print("unused")
    else:
        print("Неправильный IP-адрес2")

    
