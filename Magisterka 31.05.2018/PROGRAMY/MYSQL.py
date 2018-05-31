#strona MYSQL/connector
import time
import mysql.connector

try:
    cnx = mysql.connector.connect(user = 'root', password = 'antek666', database = 'zgrzewarka_dane')
    mycursor = cnx.cursor()
    #mycursor.execute("USE zgrzewarka_users")
    mycursor.execute("SHOW TABLES")
    print(mycursor.fetchall())
    
    mycursor.execute("SELECT * FROM parametry")
    TAK = mycursor.fetchall()
    PWM = TAK[0][1]
    print(PWM)
    print("udane poczenie z bazą danych")
    cnx.close()
    
except:
    print("NIEudane poczenie z bazą danych")
