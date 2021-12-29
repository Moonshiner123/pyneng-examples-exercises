# -*- coding: utf-8 -*-

"""
Задание 22.1d

Изменить класс Topology из задания 22.1c

Добавить метод add_link, который добавляет указанное соединение, если его еще
 нет в топологии.
Если соединение существует, вывести сообщение "Такое соединение существует",
Если одна из сторон есть в топологии, вывести сообщение
"Cоединение с одним из портов существует"


Создание топологии
In [7]: t = Topology(topology_example)

In [8]: t.topology
Out[8]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [9]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))

In [10]: t.topology
Out[10]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [11]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
Такое соединение существует

In [12]: t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
Cоединение с одним из портов существует


"""
from pprint import pprint

class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)
        
    def _normalize(self, topology_dict):
        topo = {}
        for key, value in topology_dict.items():
            if not topo.get(value) == key:
                topo[key] = value
        return topo
    
    def delete_link(self, local_end, remote_end):
        match = False
        for key, value in self.topology.copy().items():
            if key == local_end and value == remote_end or key == remote_end and value == local_end:
                del self.topology[key]
                match = True
        if match == False:
            print('Такого соединения нет')
    
    def delete_node(self, node):
        match = False
        for key, value in self.topology.copy().items():
            if node in key or node in value:
                del self.topology[key]
                match = True
        if match == False:
            print('Такого устройства нет')
            
    def add_link(self, local_end, remote_end):
        keys_and_values = self.topology.keys() | self.topology.values()
        pprint(f' Keys and values: {keys_and_values}')
        check_if_link_exists = False
        check_if_one_end_exists = False
        for key, value in self.topology.copy().items():
            if key == local_end or value == remote_end or key == remote_end or value == local_end:
                check_if_one_end_exists = True
                if key == local_end and value == remote_end or key == remote_end and value == local_end:
                    check_if_link_exists = True     
        if check_if_link_exists == True:
            print('Такое соединение существует')       
        elif check_if_one_end_exists == True:
            print('Cоединение с одним из портов существует') 
        else:            
            self.topology[local_end] = remote_end
        
        
                

        

if __name__ == "__main__":
    topology_example = {
        ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
        ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
        ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
        ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
        ("R3", "Eth0/1"): ("R4", "Eth0/0"),
        ("R3", "Eth0/2"): ("R5", "Eth0/0"),
        ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
        ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
        ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
    }
    
    print("Topology init")
    t = Topology(topology_example)
    pprint(t.topology)

    t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
    pprint(t.topology)
    t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/0'))
    t.add_link(('R1', 'Eth0/4'), ('R7', 'Eth0/5'))
    
