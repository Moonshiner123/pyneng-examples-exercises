# -*- coding: utf-8 -*-
"""
Задание 7.2b

Переделать скрипт из задания 7.2a: вместо вывода на стандартный поток вывода,
скрипт должен записать полученные строки в файл

Имена файлов нужно передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore
и строки, которые начинаются на '!'.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

ignore = ["duplex", "alias", "configuration"]

from sys import argv
src_file=argv[1]
dest_file=argv[2]

with open(f"{src_file}", "r") as src, open(f"{dest_file}", "w") as dest:
    for line in src:
        if line[0]=="!":
            pass
        elif set(line.split()) & set(ignore):
            pass
        else:
            dest.write(line)
