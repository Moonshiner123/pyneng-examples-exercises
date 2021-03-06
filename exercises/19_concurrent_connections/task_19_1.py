# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции ping_ip_addresses:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""

import subprocess
from concurrent.futures import ThreadPoolExecutor
import logging
from datetime import datetime
import time

start_time = datetime.now()



logging.basicConfig(
    format='%(threadName)s %(name)s %(levelname)s: %(message)s',
    level=logging.INFO)
    

def ping_ip(ip_address):
    '''
    Ping one IP
    '''
    reply = subprocess.run(['ping', '-c', '3', '-n', ip_address],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           encoding='utf-8')
    if reply.returncode == 0:
        return True
    else:
        return False
        
        
def ping_ip_addresses(ip_list, limit=3):
    '''
    Ping multiple IPs in multiple threads
    '''
    good = []
    bad = []
    logging.info("Starting pinging of devices from your list, please wait...")
    logging.info(f'Using {limit} workers')
    with ThreadPoolExecutor(max_workers=limit) as executor:
        future_list = []
        for ip in ip_list:
            future = executor.submit(ping_ip, ip)
            future_list.append(future)
        for ip, f in zip(ip_list,future_list):
            #print(f'IP: {ip}, Result: {f.result()}')
            if f.result() == True:
                good.append(ip)
            else:
                bad.append(ip)
        return good, bad
            
        

if __name__ == "__main__":
    ip_list = ["a", "4.4.4.4", "8.8.4.4", "123.234.345.456", "123", "456", "789"]
    print(ping_ip_addresses(ip_list, limit=10))
    print(f'Время выполнения скрипта: {datetime.now() - start_time}')


