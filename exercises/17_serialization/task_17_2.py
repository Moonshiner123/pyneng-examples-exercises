# -*- coding: utf-8 -*-
"""
Задание 17.2

В этом задании нужно:
* взять содержимое нескольких файлов с выводом команды sh version
* распарсить вывод команды с помощью регулярных выражений
  и получить информацию об устройстве
* записать полученную информацию в файл в CSV формате

Для выполнения задания нужно создать две функции.

Функция parse_sh_version:
* ожидает как аргумент вывод команды sh version одной строкой (не имя файла)
* обрабатывает вывод, с помощью регулярных выражений
* возвращает кортеж из трёх элементов:
 * ios - в формате "12.4(5)T"
 * image - в формате "flash:c2800-advipservicesk9-mz.124-5.T.bin"
 * uptime - в формате "5 days, 3 hours, 3 minutes"

У функции write_inventory_to_csv должно быть два параметра:
 * data_filenames - ожидает как аргумент список имен файлов с выводом sh version
 * csv_filename - ожидает как аргумент имя файла (например, routers_inventory.csv),
   в который будет записана информация в формате CSV
* функция записывает содержимое в файл, в формате CSV и ничего не возвращает


Функция write_inventory_to_csv должна делать следующее:
* обработать информацию из каждого файла с выводом sh version:
 * sh_version_r1.txt, sh_version_r2.txt, sh_version_r3.txt
* с помощью функции parse_sh_version, из каждого вывода должна быть получена
  информация ios, image, uptime
* из имени файла нужно получить имя хоста
* после этого вся информация должна быть записана в CSV файл

В файле routers_inventory.csv должны быть такие столбцы (именно в этом порядке):
* hostname, ios, image, uptime

В скрипте, с помощью модуля glob, создан список файлов, имя которых начинается
на sh_vers. Вы можете раскомментировать строку print(sh_version_files),
чтобы посмотреть содержимое списка.

Кроме того, создан список заголовков (headers), который должен быть записан в CSV.
"""

import glob
import re
import csv

def parse_sh_version(input_string):
    regex = (r'Cisco IOS Software.*? Version (?P<ios>\S+), .*'
             r'router uptime is (?P<uptime>\d+ days, \d+ hours, \d+ minutes).*'
             r'System image file is \"(?P<image>.+?)\"')
    match = re.search(regex, input_string, re.DOTALL)     
    return match.group('ios', 'image', 'uptime')
    
    
def write_inventory_to_csv(input_file_list, output_file):
    headers = ["hostname", "ios", "image", "uptime"]
    with open(output_file, "w") as dest:
        writer = csv.writer(dest, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(headers)
        for filename in input_file_list:
            hostname = re.search(r'sh_version_(?P<hostname>\S+).txt', filename).group(1)
            with open(filename) as f:
                current_tuple = parse_sh_version(f.read())
                #print(current_tuple)
                writer.writerow((hostname, ) + current_tuple)

    
if __name__ == "__main__":
    sh_version_files = glob.glob("sh_vers*")
    #print(sh_version_files)    
    write_inventory_to_csv(sh_version_files, 'routers_inventory.csv')
