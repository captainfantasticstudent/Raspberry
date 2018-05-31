import time

l_czas_str = ['', '', '', '', '', '']

l_czas = time.localtime()
for x in range(6):
    if (l_czas[x] > 9):
        l_czas_str[x] = str(l_czas[x])
    else:
        l_czas_str[x] = '0' + str(l_czas[x])
    print(l_czas_str[x])

    
l_data_str = str(l_czas[0]) + '-' + str(l_czas[1]) + '-' + str(l_czas[2])
print(l_data_str)
l_czas_str = str(l_czas[3]) + '.' + str(l_czas[4]) + '.' + str(l_czas[5])
print(l_czas_str)
l_file_name = "/home/ftpuser/download/" + l_data_str + '_' + l_czas_str + ".txt"
print(l_file_name)
