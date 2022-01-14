# -*- coding: utf-8 -*-

"""
Задание 23.3

Скопировать и изменить класс Topology из задания 22.1x.

Добавить метод, который позволит выполнять сложение двух экземпляров класса Topology.
В результате сложения должен возвращаться новый экземпляр класса Topology.

Создание двух топологий:

In [1]: t1 = Topology(topology_example)

In [2]: t1.topology
Out[2]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [3]: topology_example2 = {('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
                             ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}

In [4]: t2 = Topology(topology_example2)

In [5]: t2.topology
Out[5]: {('R1', 'Eth0/4'): ('R7', 'Eth0/0'), ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}

Суммирование топологий:

In [6]: t3 = t1+t2

In [7]: t3.topology
Out[7]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R1', 'Eth0/4'): ('R7', 'Eth0/0'),
 ('R1', 'Eth0/6'): ('R9', 'Eth0/0'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

Проверка, что исходные топологии не изменились:

In [9]: t1.topology
Out[9]:
{('R1', 'Eth0/0'): ('SW1', 'Eth0/1'),
 ('R2', 'Eth0/0'): ('SW1', 'Eth0/2'),
 ('R2', 'Eth0/1'): ('SW2', 'Eth0/11'),
 ('R3', 'Eth0/0'): ('SW1', 'Eth0/3'),
 ('R3', 'Eth0/1'): ('R4', 'Eth0/0'),
 ('R3', 'Eth0/2'): ('R5', 'Eth0/0')}

In [10]: t2.topology
Out[10]: {('R1', 'Eth0/4'): ('R7', 'Eth0/0'), ('R1', 'Eth0/6'): ('R9', 'Eth0/0')}
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

    #def __iter__(self):
        #print('Вызываю __iter__')
        #return iter(self.topology)
        
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
    
    topology_example2 = {
        ("R1", "Eth0/4"): ("R7", "Eth0/0"),
        ("R1", "Eth0/6"): ("R9", "Eth0/0"),
    }
    
    
    
    t1 = Topology(topology_example)
    print('\nt1:   \n', t1.topology)
    t2 = Topology(topology_example2)
    print('\nt2:   \n',t2.topology)
    t3 = t1+t2
    print('\nt3:   \n',t3.topology)
    print(t1.topology)
    print(t2.topology)
