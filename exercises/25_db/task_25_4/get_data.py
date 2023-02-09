import sqlite3
import sys
from tabulate import tabulate

db_filename = 'dhcp_snooping.db'

keys = ['mac', 'ip', 'vlan', 'interface', 'switch', 'active']
query_dict_1 = {key:"select * from dhcp where ({} = ? and active = 1)".format(key) for key in keys}
query_dict_0 = {key:"select * from dhcp where ({} = ? and active = 0)".format(key) for key in keys}

key = ''
value = ''

conn = sqlite3.connect(db_filename)

if len(sys.argv) == 1:
    print('В таблице dhcp такие записи:\n')
    print('Активные записи:\n')
    result = conn.execute("select * from dhcp where active = 1")
    print(tabulate(result, headers = keys))
    if conn.execute("select * from dhcp where active = 0").fetchall():
        print('\nНеактивные записи:\n')
        result = conn.execute("select * from dhcp where active = 0")
        print(tabulate(result, headers = keys))
            
elif len(sys.argv) != 3:
    print('Пожалуйста, введите два или ноль аргументов')
else:
    key, value = sys.argv[1:]
    if not key in keys:
        print('\nДанный параметр не поддерживается.\nДопустимые значения параметров: {}'.format(', '.join(keys)))
    else:
        print('\nИнформация об устройствах с такими параметрами:', key, value)
        query = query_dict_1[key]
        result = conn.execute(query, (value, ))
        print(tabulate(result, headers = keys))
        if conn.execute(query_dict_0[key],(value, )).fetchall():
            print('\nНеактивные записи:\n')
            query = query_dict_0[key]
            result = conn.execute(query, (value, ))
            print(tabulate(result, headers = keys))
    



