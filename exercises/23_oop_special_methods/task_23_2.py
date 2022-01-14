# -*- coding: utf-8 -*-

"""
Задание 23.2

Скопировать класс CiscoTelnet из любого задания 22.2x и добавить классу поддержку
работы в менеджере контекста.
При выходе из блока менеджера контекста должно закрываться соединение.

Пример работы:

In [14]: r1_params = {
    ...:     'ip': '192.168.100.1',
    ...:     'username': 'cisco',
    ...:     'password': 'cisco',
    ...:     'secret': 'cisco'}

In [15]: from task_23_2 import CiscoTelnet

In [16]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:
sh clock
*19:17:20.244 UTC Sat Apr 6 2019
R1#

In [17]: with CiscoTelnet(**r1_params) as r1:
    ...:     print(r1.send_show_command('sh clock'))
    ...:     raise ValueError('Возникла ошибка')
    ...:
sh clock
*19:17:38.828 UTC Sat Apr 6 2019
R1#
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-17-f3141be7c129> in <module>
      1 with CiscoTelnet(**r1_params) as r1:
      2     print(r1.send_show_command('sh clock'))
----> 3     raise ValueError('Возникла ошибка')
      4

ValueError: Возникла ошибка
"""

import telnetlib
import time
from pprint import pprint
import re
import yaml
from textfsm import clitable
from tabulate import tabulate
    
class CiscoTelnet:

    def __init__(self, ip, username, password, secret):
        self.ip = ip
        self.telnet = telnetlib.Telnet(ip)
        self.telnet.read_until(b"Username")
        self._write_line(username)
        #print('Entered username')
        self.telnet.read_until(b"Password")
        self._write_line(password)
        #print('Entered password')
        index, m, output = self.telnet.expect([b">", b"#"])
        if index == 0:
            self._write_line("enable")
            #print('Entered enable')
            self.telnet.read_until(b"Password")
            self._write_line(secret)
            #print('Entered enable secret')
            self.telnet.read_until(b"#", timeout=5)
        self._write_line("terminal length 0")
        #print('Entered terminal length 0')
        time.sleep(1)
        self.telnet.read_very_eager()

        
    def _write_line(self, line):
        return self.telnet.write(line.encode("ascii") + b"\n")
        
    def send_show_command(self, line, parse=True, templates="/home/python/repos/pyneng-examples-exercises/exercises/22_oop_basics/templates", index="index"):
        self._write_line(line)
        #print(f"Send command: {line}")
        time.sleep(1)
        output = self.telnet.read_very_eager().decode("ascii")
        if parse == False:
            return output
        else:
            cli_table = clitable.CliTable(index, templates)
            attributes = {'Command': line, 'Vendor': 'cisco_ios'}
            cli_table.ParseCmd(output, attributes)
            header = list(cli_table.header)
            data_rows = [list(row) for row in cli_table]
            result = [dict(zip(header, row)) for row in data_rows]
            return result
            
    def send_config_commands(self, cfg, strict=True):
        full_output = []
        if type(cfg) == str:
            cfg = [cfg]
        self._write_line("conf t")
        #print(f"Send command: conf t")
        time.sleep(1)
        for command in cfg:
            #print(f"Send command: {command}")
            self._write_line(command)
            time.sleep(1)
            output = self.telnet.read_very_eager().decode("ascii")
            if "%" in output:
                regex = r'% (.*)\n'
                match = re.search(regex, output).group(1)
                if strict == True:
                    raise ValueError(f'При выполнении команды "{command}" на устройстве {self.ip} возникла ошибка -> {match}')
                else:
                    print(f'При выполнении команды "{command}" на устройстве {self.ip} возникла ошибка -> {match}')
            full_output.append(output)
        self._write_line("end")
        time.sleep(1)
        full_output.append(self.telnet.read_very_eager().decode("ascii"))
        return "".join(full_output)

    def __enter__(self):
        print('Метод __enter__')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print('Метод __exit__')
        self.telnet.close()

if __name__ == "__main__":

    r1_params = {
    'ip': '192.168.100.1',
    'username': 'cisco',
    'password': 'cisco',
    'secret': 'cisco'}
    with CiscoTelnet(**r1_params) as r1:
        pprint(r1.send_show_command('sh clock'))
        
    with CiscoTelnet(**r1_params) as r1:
        pprint(r1.send_show_command('sh clock'))
        raise ValueError('Возникла ошибка')
