import time
import serial

end = 0     #zmienna oznaczająca warunkowe zatrzymanie programu

try:
    ser = serial.Serial("/dev/ttyUSB0")	#Przypisanie przejściówki UART podłączonej do wejścia USB (lista urządzeń komendą "dmesg | grep tty" bądź "ls -l dev/")
    ser.baundrate = 9600
    print("Konfiguracja USBtty poprawna")
except:
    print("Konfiguracja USBtty nieudana, sprawdź ustawienia")
    end = 1

while (end == 0):
    print("Data to send: ")
    zmienna1 = input()
    zmienna1 = zmienna1 + '\n'		#dodanie znaku końca linii
    ser.write(zmienna1.encode())	#wypisz zmienną poprzez UART
    print('Send data: ', zmienna1)	#wypisz profilaktycznie w konsoli zmienną
        
