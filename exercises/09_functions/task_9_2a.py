# -*- coding: utf-8 -*-
"""
Задание 9.2a

Сделать копию функции generate_trunk_config из задания 9.2

Изменить функцию таким образом, чтобы она возвращала не список команд, а словарь:
- ключи: имена интерфейсов, вида 'FastEthernet0/1'
- значения: список команд, который надо
  выполнить на этом интерфейсе

Проверить работу функции на примере словаря trunk_config и шаблона trunk_mode_template.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""


trunk_mode_template = [
    "switchport mode trunk",
    "switchport trunk native vlan 999",
    "switchport trunk allowed vlan",
]

trunk_config = {
    "FastEthernet0/1": [10, 20, 30],
    "FastEthernet0/2": [11, 30],
    "FastEthernet0/4": [17],
}



def generate_trunk_config(intf_vlan_mapping, trunk_template):
    '''
    My third fucking function
    '''
    config_dict={}
    for intf, vlans in intf_vlan_mapping.items():
        config=[]
        interface=f'interface {intf}'
        config_dict.setdefault(interface)
        for command in trunk_template:
            if command.endswith('allowed vlan'):
                vlan=",".join([str(i) for i in vlans])
                config.append(f'{command} {vlan}')
            else:
                config.append({f'{command}'})
        config_dict.update({interface: config})
    return config_dict


print(generate_trunk_config(trunk_config, trunk_mode_template))
