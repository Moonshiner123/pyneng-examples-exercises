# -*- coding: utf-8 -*-

"""
Задание 22.2

Создать класс CiscoTelnet, который подключается по Telnet к оборудованию Cisco.

При создании экземпляра класса, должно создаваться подключение Telnet, а также
переход в режим enable.
Класс должен использовать модуль telnetlib для подключения по Telnet.

У класса CiscoTelnet, кроме __init__, должно быть, как минимум, два метода:
* _write_line - принимает как аргумент строку и отправляет на оборудование строку
  преобразованную в байты и добавляет перевод строки в конце. Метод _write_line должен
  использоваться внутри класса.
* send_show_command - принимает как аргумент команду show и возвращает вывод
  полученный с обрудования

Параметры метода __init__:
* ip - IP-адрес
* username - имя пользователя
* password - пароль
* secret - пароль enable

Пример создания экземпляра класса:
In [2]: from task_22_2 import CiscoTelnet

In [3]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}
   ...:

In [4]: r1 = CiscoTelnet(**r1_params)

In [5]: r1.send_show_command("sh ip int br")
Out[5]: 'sh ip int br\r\nInterface                  IP-Address      OK? Method Status                Protocol\r\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \r\nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \r\nEthernet0/2                unassigned      YES manual up                    up      \r\nEthernet0/3                192.168.130.1   YES NVRAM  up                    up      \r\nR1#'


Подсказка:
Метод _write_line нужен для того чтобы можно было сократить строку:
self.telnet.write(line.encode("ascii") + b"\n")

до такой:
self._write_line(line)

Он не должен делать ничего другого.
"""

class CiscoTelnet:
    
    import telnetlib
    import time
    from pprint import pprint

    def __init__(self, ip, username, password, secret):
        self.ip, self.username, self.password, self.secret = ip, username, password, secret
        with telnetlib.Telnet(self.ip) as telnet:
            telnet.read_until(b"Username")
            telnet._write_line(self.username)
            telnet.read_until(b"Password")
            telnet._write_line(self.password)
            index, m, output = telnet.expect([b">", b"#"])
            if index == 0:
                telnet._write_line(b"enable\n")
                telnet.read_until(b"Password")
                telnet._write_line(self.secret)
                telnet.read_until(b"#", timeout=5)
            telnet._write_line(b"terminal length 0\n")
            telnet.read_until(b"#", timeout=5)
        
    def _write_line(self, line):
        return f"{line}\n".encode("utf-8")
