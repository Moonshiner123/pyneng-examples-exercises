# -*- coding: utf-8 -*-

"""
Задание 23.3a

В этом задании надо сделать так, чтобы экземпляры класса Topology
были итерируемыми объектами.
Основу класса Topology можно взять из любого задания 22.1x или задания 23.3.

После создания экземпляра класса, экземпляр должен работать как итерируемый объект.
На каждой итерации должен возвращаться кортеж, который описывает одно соединение.
Порядок вывода соединений может быть любым.


Пример работы класса:

In [1]: top = Topology(topology_example)

In [2]: for link in top:
   ...:     print(link)
   ...:
(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
(('R2', 'Eth0/1'), ('SW2', 'Eth0/11'))
(('R3', 'Eth0/0'), ('SW1', 'Eth0/3'))
(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))


Проверить работу класса.
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

    def __add__(self, other):
        print('\nadding...\nOriginal topology:\n', self.topology)
        print('\nadding...\nSecond topology:\n', other.topology)
        summary_topology = self.topology.copy()
        summary_topology.update(other.topology)
        print('\nSummary: \n', summary_topology)
        return Topology(summary_topology)

    def __iter__(self):
        print('Вызываю __iter__')
        return iter(self.topology.items())
        
    def __str__(self):
        return f"Topology representation: {self.topology}"
            
    def __repr__(self):
        return f"Topology('{self.topology}')"
        
        
        
        
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

    
    
    t1 = Topology(topology_example)
    pprint(t1.topology)
    for link in t1:
        print(link)
