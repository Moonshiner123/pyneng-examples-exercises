# -*- coding: utf-8 -*-
"""
Задание 17.4

Создать функцию write_last_log_to_csv.

Аргументы функции:
* source_log - имя файла в формате csv, из которого читаются данные (mail_log.csv)
* output - имя файла в формате csv, в который будет записан результат

Функция ничего не возвращает.

Функция write_last_log_to_csv обрабатывает csv файл mail_log.csv.
В файле mail_log.csv находятся логи изменения имени пользователя. При этом, email
пользователь менять не может, только имя.

Функция write_last_log_to_csv должна отбирать из файла mail_log.csv только
самые свежие записи для каждого пользователя и записывать их в другой csv файл.
В файле output первой строкой должны быть заголовки столбцов,
такие же как в файле source_log.

Для части пользователей запись только одна и тогда в итоговый файл надо записать
только ее.
Для некоторых пользователей есть несколько записей с разными именами.
Например пользователь с email c3po@gmail.com несколько раз менял имя:
C=3PO,c3po@gmail.com,16/12/2019 17:10
C3PO,c3po@gmail.com,16/12/2019 17:15
C-3PO,c3po@gmail.com,16/12/2019 17:24

Из этих трех записей, в итоговый файл должна быть записана только одна - самая свежая:
C-3PO,c3po@gmail.com,16/12/2019 17:24

Для сравнения дат удобно использовать объекты datetime из модуля datetime.
Чтобы упростить работу с датами, создана функция convert_str_to_datetime - она
конвертирует строку с датой в формате 11/10/2019 14:05 в объект datetime.
Полученные объекты datetime можно сравнивать между собой.
Вторая функция convert_datetime_to_str делает обратную операцию - превращает
объект datetime в строку.

Функции convert_str_to_datetime и convert_datetime_to_str использовать не обязательно.

"""

import datetime
import csv
from pprint import pprint


def convert_str_to_datetime(datetime_str):
    """
    Конвертирует строку с датой в формате 11/10/2019 14:05 в объект datetime.
    """
    return datetime.datetime.strptime(datetime_str, "%d/%m/%Y %H:%M")


def convert_datetime_to_str(datetime_obj):
    """
    Конвертирует строку с датой в формате 11/10/2019 14:05 в объект datetime.
    """
    return datetime.datetime.strftime(datetime_obj, "%d/%m/%Y %H:%M")
    

def write_last_log_to_csv(source_log, output=None): 
    '''
    Сначала преобразуем данные из csv в список.
    '''
    log_list = []
    with open(source_log) as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            log_list.append(row)
    sorted_by_mail = sorted(log_list, key=lambda x: x[1])
    '''
    Затем отсортируем список по имейлу и превратим его в словарь (Чтобы для key=email более новые значения date+name перезаписывали предыдущие).
    '''
    sorted_dict = {}
    prev_name,prev_mail,prev_date = sorted_by_mail[0]
    for log in sorted_by_mail:
        #print(log)
        name, mail, date = log
        if mail == prev_mail:
            #print('prev_date: ' + str(convert_str_to_datetime(prev_date)))
            #print('curr_date: ' + str(convert_str_to_datetime(date)))
            if convert_str_to_datetime(date)>=convert_str_to_datetime(prev_date):
                sorted_dict.update({mail: [name, date]})
                prev_name,prev_date = name,date
                #pprint(sorted_dict)l
        else:
            sorted_dict.update({mail: [name, date]})
            #pprint(sorted_dict)
        prev_mail = mail
        #print('='*40)
    '''
    Наконец, преобразуем данные в первоначальный вид и в CSV-форматд
    ''' 
    final_list = []
    for key, value in sorted_dict.items():  
        final_list.append([value[0], key, value[1]])
    with open(output, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in final_list:
            writer.writerow(row)




if __name__ == "__main__":
    write_last_log_to_csv('mail_log.csv', 'output.csv')
    with open('output.csv') as f:
        print(f.read())

