# -*- coding: utf-8 -*-

"""
Задание 22.1c

Изменить класс Topology из задания 22.1b.

Добавить метод delete_node, который удаляет все соединения с указаным устройством.

Если такого устройства нет, выводится сообщение "Такого устройства нет".

Создание топологии
In [1]: t = Topology(topology_example)

In [2]: t.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Удаление устройства:
In [3]: t.delete_node('SW1')

In [4]: t.topology
Out[4]:
{('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Если такого устройства нет, выводится сообщение:
In [5]: t.delete_node('SW1')
Такого устройства нет

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
    print(t.topology)
    print("\nDeleting SW1 node...")
    t.delete_node('SW1')
    print(t.topology)
    print("\nDeleting SW2 node...")
    t.delete_node('SW2')
    print(t.topology)
    

