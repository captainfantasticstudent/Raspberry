import time
import serial

ser = serial.Serial("/dev/ttyUSB1")	#Przypisanie przejściówki UART podłączonej do wejścia USB (lista urządzeń komendą "dmesg | grep tty" bądź "ls -l dev/")
ser.baundrate = 9600

while 1:
    zmienna = 123231			#zmienna do wypisania przez UART
    zmienna1 = str(zmienna)		#zamiana zmiennej na łańcuch znaków
    zmienna1 = zmienna1 + '\n'		#dodanie znaku końca linii
    print(zmienna1)			#wypisz progilaktycznie w konsoli zmienną
    ser.write(zmienna1.encode())	#wypisz zmienną poprzez UART
    time.sleep(1)
        
