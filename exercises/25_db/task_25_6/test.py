import re
'''
Функция делает список имен файлов из пользовательского ввода типа 
sw[1-3]_dhcp_snooping.txt
'''
user_input = 'sw[1-3]_dhcp_snooping.txt'

user_input_regex = r'(?P<letters_part>\S+?)(?P<numbers_part>\[\d+-\d+\])?_dhcp_snooping.txt'
sw_name = re.search(user_input_regex,user_input)
print(sw_name.group('letters_part'))
print(sw_name.group('numbers_part'))
if not sw_name.group('numbers_part'):
    result = [sw_name.group('letters_part') + '_dhcp_snooping.txt']
else:
    numbers_part = sw_name.group('numbers_part')
    numbers_part_regex = r'\[(?P<number_1>\d+)-(?P<number_2>\d+)\]'
    numbers = re.search(numbers_part_regex, numbers_part)
    number_1 = int(numbers.group('number_1'))
    number_2 = int(numbers.group('number_2')) + 1
    result = [sw_name.group('letters_part') + str(number) + '_dhcp_snooping.txt' for number in range(number_1, number_2)]
print(result)
