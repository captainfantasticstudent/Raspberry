import mysql.connector
import time

l_czas = time.localtime()
l_data_str = str(l_czas[0]) + '-' + str(l_czas[1]) + '-' + str(l_czas[2])
#print(data_str)
l_czas_str = str(l_czas[3]) + '.' + str(l_czas[4]) + '.' + str(l_czas[5])
l_file_name = l_data_str + '_' + l_czas_str + ".txt"

l_cnx = mysql.connector.connect(user = 'root',
                                password = 'antek666',
                                database = 'zgrzewarka_dane')
l_mycursor = l_cnx.cursor()
l_SQLcommand = "INSERT INTO pomiary VALUES (NULL,'" + l_data_str + "', '"  + l_czas_str +  "','" + l_file_name + "');"
l_mycursor.execute(l_SQLcommand)
l_cnx.commit()

l_SQLcommand = 'SELECT * FROM pomiary'
l_mycursor.execute(l_SQLcommand)

message = l_mycursor.fetchall()
print(message)


#l_cnx.commit()
l_cnx.close()
