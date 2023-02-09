import sqlite3
import sys
from tabulate import tabulate

db_filename = 'dhcp_snooping.db'

keys = ['mac', 'ip', 'vlan', 'interface', 'switch', 'active', 'last_active']
query_dict = {key:"select * from dhcp where {} = ?".format(key) for key in keys}

key = ''
value = ''

conn = sqlite3.connect(db_filename)

if len(sys.argv) == 1:
    print('\nВ таблице dhcp такие записи:')
    result = conn.execute("select * from dhcp")
    print(tabulate(result, headers = keys))
elif len(sys.argv) != 3:
    print('Пожалуйста, введите два или ноль аргументов')
else:
    key, value = sys.argv[1:]
    if not key in keys:
        print('\nДанный параметр не поддерживается.\nДопустимые значения параметров: {}'.format(', '.join(keys)))
    else:
        print('\nИнформация об устройствах с такими параметрами:', key, value)
        query = query_dict[key]
        result = conn.execute(query, (value, ))
        print(tabulate(result, headers = keys))       

    



