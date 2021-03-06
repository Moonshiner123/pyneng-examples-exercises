# -*- coding: utf-8 -*-

"""
Задание 22.2c

Скопировать класс CiscoTelnet из задания 22.2b и изменить метод send_config_commands
добавив проверку команд на ошибки.

У метода send_config_commands должен быть дополнительный параметр strict:
* strict=True значит, что при обнаружении ошибки, необходимо сгенерировать
  исключение ValueError (значение по умолчанию)
* strict=False значит, что при обнаружении ошибки, надо только вывести
  на стандартный поток вывода сообщене об ошибке

Метод дожен возвращать вывод аналогичный методу send_config_set
у netmiko (пример вывода ниже). Текст исключения и ошибки в примере ниже.

Пример создания экземпляра класса:
In [1]: from task_22_2c import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

In [4]: commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
In [5]: correct_commands = ['logging buffered 20010', 'ip http server']
In [6]: commands = commands_with_errors+correct_commands

Использование метода send_config_commands:

In [7]: print(r1.send_config_commands(commands, strict=False))
При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.
При выполнении команды "logging" на устройстве 192.168.100.1 возникла ошибка -> Incomplete command.
При выполнении команды "a" на устройстве 192.168.100.1 возникла ошибка -> Ambiguous command:  "a"
conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#a
% Ambiguous command:  "a"
R1(config)#logging buffered 20010
R1(config)#ip http server
R1(config)#end
R1#

In [8]: print(r1.send_config_commands(commands, strict=True))
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-8-0abc1ed8602e> in <module>
----> 1 print(r1.send_config_commands(commands, strict=True))

...

ValueError: При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.

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
        
    def send_show_command(self, line, parse=True, templates="templates", index="index"):
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

            

if __name__ == "__main__":

    r1_params = {
    'ip': '192.168.100.1',
    'username': 'cisco',
    'password': 'cisco',
    'secret': 'cisco'}
    r1 = CiscoTelnet(**r1_params)
    commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
    correct_commands = ['logging buffered 20010', 'ip http server']
    commands = commands_with_errors+correct_commands
    print(r1.send_config_commands(commands, strict=False))
    #print(r1.send_config_commands(commands, strict=True))
