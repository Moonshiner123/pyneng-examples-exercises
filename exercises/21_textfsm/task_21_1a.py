# -*- coding: utf-8 -*-
"""
Задание 21.1a

Создать функцию parse_output_to_dict.

Параметры функции:
* template - имя файла, в котором находится шаблон TextFSM.
  Например, templates/sh_ip_int_br.template
* command_output - вывод соответствующей команды show (строка)

Функция должна возвращать список словарей:
* ключи - имена переменных в шаблоне TextFSM
* значения - части вывода, которые соответствуют переменным

Проверить работу функции на выводе команды output/sh_ip_int_br.txt
и шаблоне templates/sh_ip_int_br.template.
"""

from netmiko import ConnectHandler
import textfsm
from tabulate import tabulate


def parse_output_to_dict(template, command_output):
    result = []
    with open(template) as f:
        re_table = textfsm.TextFSM(f)
        header = re_table.header
        data = re_table.ParseText(command_output)
        for element in data:
            dict_element = dict(zip(header, element))
            result.append(dict_element)
        return result

# вызов функции должен выглядеть так
if __name__ == "__main__":
    r1_params = {
        "device_type": "cisco_ios",
        "host": "192.168.100.1",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }

    with ConnectHandler(**r1_params) as r1:
        r1.enable()
        output = r1.send_command("sh ip int br")

    result = parse_output_to_dict("templates/sh_ip_int_br.template", output)
    print(result)
    print(tabulate(result))
