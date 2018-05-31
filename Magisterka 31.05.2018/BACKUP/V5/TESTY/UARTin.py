import time
import serial

UART = 0
czas = 0

def wpisz(l_plik = '', l_dane = 0):
    path = l_plik + ".txt"
    f = open(path, "a")
    f.write(str(l_dane))
    f.close()
    


try:
    ser = serial.Serial("/dev/ttyUSB0")	#Przypisanie przejściówki UART podłączonej do wejścia USB (lista urządzeń komendą "dmesg | grep tty" bądź "ls -l dev/")
    ser.baundrate = 9600
    print("# Konfiguracja USBtty poprawna")
    print("# Port USBtty:" + ser.name)
except:
    print("! Konfiguracja USBtty nieudana, sprawdź ustawienia")
    print("! numer portu USBtty prawdopodobnie sie nie zgadza")
    end = 1

f = open("plik.txt", "w") #"a"			- tryb dopisywanioa na końcu pliku tekstu
#f.write("tekst")	- wpisanie do pliku tekstu
f.close
#f.read()		- odczytanie danych z otwartego pliku
#f.readline()		- odczytanie całej linii z pliku
liczba_1 = 0
liczba_2 = 0
#czyszczenie bufora rejestru UART
while 1:
    while(ser.inWaiting()):
        UART = ser.read()
        if(int.from_bytes(UART, byteorder = 'big') != 255):
            print(int.from_bytes(UART, byteorder = 'big'), end = "")
            print('\n')
        #if(UART == "\n"):
        #    czas = czas + 0.1
        #    UART = ';' + str(czas) + UART 
        #wpisz("plik", UART)
