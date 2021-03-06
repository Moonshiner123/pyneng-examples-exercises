# -*- coding: utf-8 -*-

"""
Задание 23.1a

Скопировать и изменить класс IPAddress из задания 23.1.

Добавить два строковых представления для экземпляров класса IPAddress.
Как дожны выглядеть строковые представления, надо определить из вывода ниже:

Создание экземпляра
In [5]: ip1 = IPAddress('10.1.1.1/24')

In [6]: str(ip1)
Out[6]: 'IP address 10.1.1.1/24'

In [7]: print(ip1)
IP address 10.1.1.1/24

In [8]: ip1
Out[8]: IPAddress('10.1.1.1/24')

In [9]: ip_list = []

In [10]: ip_list.append(ip1)

In [11]: ip_list
Out[11]: [IPAddress('10.1.1.1/24')]

In [12]: print(ip_list)
[IPAddress('10.1.1.1/24')]

"""
class IPAddress:
    def __init__(self, ipmask):
        self._check_ip(ipmask)
        self._check_mask(ipmask)
        
    def _check_mask(self, ipmask):
        self.mask = int(ipmask.split('/')[1])
        print('Проверка MASK...')
        if not (8 <= self.mask <= 32):
            raise ValueError('Incorrect mask')
    
    def _check_ip(self, ipmask):
        self.ip = ipmask.split('/')[0]
        print('Проверка IP...')
        iplist = self.ip.split('.')
        if len(iplist) == 4:
            for i in iplist:
                if int(i) not in range(256):
                     raise ValueError('Incorrect IPv4 address')
        else:
            raise ValueError('Incorrect IPv4 address')
        
    def __str__(self):
        return f"IP address {self.ip}/{self.mask}"
            
    def __repr__(self):
        return f"IPAddress('{self.ip}/{self.mask}')"
        


if __name__ == "__main__":
    ip1 = IPAddress('1.1.1.1/32')
    print(ip1.ip)
    print(ip1.mask)
    print(ip1)
    ip_list = []
    ip_list.append(ip1)
    ip_list
    print(ip_list)
    
