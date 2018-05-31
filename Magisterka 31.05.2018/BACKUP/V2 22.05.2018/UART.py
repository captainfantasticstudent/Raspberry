import time
import serial
import mysql.connector

end= 0                                  #zmienna oznaczająca warunkowe zatrzymanie programu
tabUART = ['0', '0', '0', '0', '0', '0', '0']     #tablica/lista danych z portu UART
licznikUART = 0                         #zmienna ilości znaków przechwyconych z portu UART
toMe = 0                                #czy identyfikator wiadomości do mnie 
pwm = '-'                               #wartość wypełnienia PWM
confirmFlagPWM = 0                         #flaga wymagania potwierdzenia odebrania wiadomości przez uC lub konieczności odpowiedzi
confirmFlagSTART = 0
resendPWM = 0                           #flaga konieczności ponownego przesłania wiadomości
resendSTART = 0

uC_id = {"Bb":'1'}
uC_list = ["Bb"]
uC_numbers_of = 1
uC_counter = 0

czas = 0                                #zmienne potrzebne do kontorli programu w funkcji czasu
czasH = 0
czas1 = 0
czas2 = 0


#czyszczenie bufora rejestru UART
def clearUARTbuf():
    while(ser.inWaiting()):
        ser.read()

#wpisanie wartoci (wartosc) do danej tabeli (table) w bazie danych "zgrzewarka_dane"
def SQLwrite(l_table = 'PWM', l_wartosc = '0', l_uC_id = 'Bb'):
    try:
        l_cnx = mysql.connector.connect(user = 'root', password = 'antek666', database = 'zgrzewarka_dane')
        l_mycursor = l_cnx.cursor()
        l_SQLcommand = 'UPDATE parametry SET ' + l_table + '=' + l_wartosc + ' WHERE id=' + uC_id[l_uC_id]
        l_mycursor.execute(l_SQLcommand)
        l_cnx.commit()
        l_cnx.close()
        return l_wartosc
    except:
        print("! ERROR. Nieudane wpisanie wartosci do bazy danych!")
        return l_wartosc

#odczytanie wartości tabeli (l_table) z bazy i zwrot jej wartości
def SQLread(l_table = 'PWM', l_uC_id = 'Bb'):
    try:
        l_cnx = mysql.connector.connect(user = 'root', password = 'antek666', database = 'zgrzewarka_dane')
        l_mycursor = l_cnx.cursor()
        l_SQLcommand = 'SELECT ' +  l_table + ' FROM parametry WHERE id=' + uC_id[l_uC_id]
        l_mycursor.execute(l_SQLcommand)
        l_SQLdata = l_mycursor.fetchall()
        l_cnx.close()
        return l_SQLdata[0][0]
    except:
        print("! ERROR. Odczyt z bazy danych nieudany")
        return 0

#przygotowanie bazy danych - zerowanie wartości PWM i flagi gotowosci
def SQLprepare():
    try:
        #Polaczenie z baza danych
        l_cnx = mysql.connector.connect(user = 'root', password = 'antek666')
        l_mycursor = l_cnx.cursor()
        l_mycursor.execute("USE zgrzewarka_dane")
        #zerowanie wartosci PWM i zmiennej GOTOWOSCI
        for l_x in uC_id:
            l_SQLcommand = 'UPDATE parametry SET PWM=0, GOTOWE=0, START=0 WHERE id=' + uC_id[l_x]
            l_mycursor.execute(l_SQLcommand)
            l_cnx.commit()
        print("# Udane otwarcie bazy danych")
        l_cnx.close()
    except:
        print("! ERROR. Nieudane otwarcie bazy danych")

def wpisz_do_pliku(l_plik = '', l_dane_str = ''):
    path = l_plik + ".txt"
    f = open(path, "a")
    f.write(l_dane_str)
    f.close()

def odbierz_przebiegi():
    l_time = 0
    l_time2 = 1
    l_string = ''
    l_kolejnosc = 0
    l_dane1 = 0
    l_dane2 = 0

    f = open('plik.txt', "w")
    f.close()

    while(l_time < 1.2):
        if(ser.inWaiting()):
            while(ser.inWaiting()):    
                l_UART = ser.read()
                if l_UART != b'\xff':
                    if (l_kolejnosc == 1):
                        l_dane2 = int.from_bytes(l_UART, byteorder = 'big')
                        l_dane = l_dane1 * 255 + l_dane2
                        l_string = str(l_dane) + ' ' + str(l_time2/10) + '\n'
                        wpisz_do_pliku('plik', l_string)
                        l_time2 = l_time2 + 1
                        l_kolejnosc = 0
                    else:
                        l_kolejnosc = 1
                        l_dane1 = int.from_bytes(l_UART, byteorder = 'big')
                l_time = 0
        else:
            l_time = l_time + 0.0001
            time.sleep(0.0001)
    print("$ Koniec oczekowania na dane. Gotowoc do pracy")


### MAIN PROGRAM
# odczyt i obsługa bazy danych
# wysylanie wypelnienia PWM poprzez USART
# sprawdzanie poprawności danych
### END

try:
    ser = serial.Serial("/dev/ttyUSB0")	#Przypisanie przejściówki UART podłączonej do wejścia USB (lista urządzeń komendą "dmesg | grep tty" bądź "ls -l dev/")
    ser.baundrate = 9600
    print("# Konfiguracja USBtty poprawna")
    print("# Port USBtty:" + ser.name)
except:
    print("! Konfiguracja USBtty nieudana, sprawdź ustawienia")
    print("! numer portu USBtty prawdopodobnie sie nie zgadza")
    end = 1

SQLprepare()    #wyzerowanie bazy danych

print("$ press ENTER to continue")
#input()
print("")

while(end == 0):
    while(ser.inWaiting()):
        dataUART = ser.read()
        if toMe == 2 and (confirmFlagPWM == 1 or confirmFlagSTART == 1):
            if licznikUART < 7:
                tabUART[licznikUART] = dataUART
                licznikUART = licznikUART + 1
                if licznikUART == 7:
                    if pwm[2].encode() == tabUART[4] and pwm[1].encode() == tabUART[3] and pwm[0].encode() == tabUART[2]:
                        print(tabUART)
                        print("# Poprawne przyjcie wysłanych danych przez uC")
                        clearUARTbuf()
                        licznikUART = 0
                        toMe = 0
                        confirmFlagPWM = 0
                        SQLwrite('GOTOWE', '1' , 'Bb')
                    elif tabUART[4] == b'x' and tabUART[3] == b'x' and tabUART[2] == b'x':
                        send_from = tabUART[5].decode() + tabUART[6].decode()
                        SQLwrite('START', '0', send_from)
                        print("$ POPRAWNY START ZGRZEWARKI " + send_from)

                        odbierz_przebiegi()
                        
                        confirmFlagSTART = 0
                    else:
                        print(tabUART)
                        print("! uC odebrał dane błędnie")
                        clearUARTbuf()
                        licznikUART = 0
                        toMe = 0
                        confirmFlagPWM = 0
                        resendPWM = 1
                        SQLwrite('GOTOWE', '0', 'Bb')
            else:
                print("! Odebrano bezsensowne dane")
                clearUARTbuf()
                licznikUART = 0
                toMe = 0
                resendPWM = 1
        else:
            if licznikUART == 0 and dataUART == b'C':
                toMe = 1
                tabUART[licznikUART] = dataUART
                licznikUART = licznikUART + 1
            elif toMe == 1 and dataUART == b'c':
                toMe = 2
                tabUART[licznikUART] = dataUART
                licznikUART = licznikUART + 1
            else:
                toMe = 0
                licznikUART = 0

    if (czas - czas1 >= 2) and ((confirmFlagPWM == 1) or (confirmFlagSTART == 1)):
        toMe = 0
        licznikUART = 0
        print("! uC nie odpowiedział")
        if(confirmFlagPWM == 1):
            resendPWM = 1
            confirmFlagPWM = 0
        if(confirmFlagSTART == 1):
            confirmFlagSTART = 0
            resendSTART = 1
            print(confirmFlagSTART)
        czas1 = czas

        

    if (czas - czas2 >= 0.5):
        czas2 = czas
        try:     
            PWM = SQLread('PWM', 'Bb')
            if PWM < 10:
                dane = "00" + str(PWM)
            elif PWM < 100:
                dane = "0" + str(PWM)
            else:
                dane = "000"
            
            if int(dane) < 100 and int(dane) >= 0 and len(dane) == 3:
                if pwm != dane  or resendPWM == 1:
                    pwm = dane
                    daneSTR = "Bb" + pwm + "Cc"
                    print("# wysłano do uC: " + daneSTR)
                    ser.write(daneSTR.encode())
                    confirmFlagPWM = 1
                    SQLwrite('GOTOWE', '0', 'Bb')
                    print("# Oczekiwanie na odpowiedź uC")
                    resendPWM = 0
                    czas1 = czas
            else:
                print("! Za duze wypenienie PWM lub zły format danych")
        except:
            print("! ERROR. Nie wyslano nic do uC")

        if (((SQLread('START', 'Bb') == 1 and SQLread('GOTOWE', 'Bb') == 1) or resendSTART == 1) and confirmFlagPWM == 0):
            kodPotwierdzenia = 'Bb' + "xxx" + "Cc"
            ser.write(kodPotwierdzenia.encode())
            confirmFlagSTART = 1
            resendSTART = 0
            czas1 = czas
    
    time.sleep(0.1)
    czas = czas + 0.1

    if czas == 3600:
        czasH = 1
        czas = 0
        czas1 = 0
        czas2 = 0
