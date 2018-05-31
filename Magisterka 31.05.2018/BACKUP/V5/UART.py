import time
import serial
import mysql.connector

### podstawowe zmienne programu
end= 0                                          #zmienna oznaczająca warunkowe zatrzymanie programu
tabUART = ['0', '0', '0', '0', '0', '0', '0']   #tablica/lista danych z portu UART
licznikUART = 0                                 #zmienna ilości znaków przechwyconych z portu UART
toMe = 0                                        #czy identyfikator wiadomości do mnie 
#pwm = '-'                                      #wartość wypełnienia PWM
#confirmFlagPWM = 0                             #flaga wymagania potwierdzenia odebrania wiadomości przez uC lub konieczności odpowiedzi
#resendPWM = 0                                  #flaga konieczności ponownego przesłania wiadomości
confirmFlagSTART = 0
resendSTART = 0

### zmienne potrzebne do ustawienia odpowiednich wartoci w mikrokontrolerze
values = ['-', '-']             #val[0] -> PWM, val[1] -> czas
resend = [0, 0]                 #resend[0] -> PWM, resend[1] -> czas
confirmFlag = [0, 0]            #cf[0] -> PWM, cf[1] -> czas
checkWhat = ['PWM', 'czas']     #co należy sprawdzi w bazie danych
count = 0                       #licznik
SQLdata = 0                     #dane odczytane z bazy danych  

### zmienne potrzebne w wypadku kontroli wicej ni jednego mikrokontrolera zgrzewarki
uC_id = {"Bb":'1'}
uC_list = ["Bb"]
uC_numbers_of = 1
uC_counter = 0

### zmienne potrzebne do kontorli programu w funkcji czasu
czas = 0        #czas który upłynął                                
czasH = 0       #liczba godzin która upłynęła
czas1 = 0       #zmienna potrzebna do wykonania jakiejś funkcji programu w określonym czasie
czas2 = 0       #zmienna potrzebna do wykonania jakiejś funkcji programu w określonym czasie


### czyszczenie bufora rejestru UART
def clearUARTbuf():
    while(ser.inWaiting()):
        ser.read()

### wpisanie wartoci (l_wartosc) do danej tabeli (l_table) w bazie danych "zgrzewarka_dane"
  # otwarcie bazy danych i aktualizacja wartości w niej zawartych
  # w przypadku niepowodzenia wyświetlana jest wiadomość o błędzie
###
def SQLwrite(l_table = 'PWM', l_wartosc = '0', l_uC_id = 'Bb'):
    try:
        l_cnx = mysql.connector.connect(user = 'root',
                                        password = 'antek666',
                                        database = 'zgrzewarka_dane')
        l_mycursor = l_cnx.cursor()
        l_SQLcommand = 'UPDATE parametry SET ' + l_table + '=' + l_wartosc + ' WHERE id=' + uC_id[l_uC_id]
        l_mycursor.execute(l_SQLcommand)
        l_cnx.commit()
        l_cnx.close()
        return l_wartosc
    except:
        print("! ERROR. Nieudane wpisanie wartosci do bazy danych!")
        return l_wartosc

### odczytanie wartości tabeli (l_table) z bazy i zwrot jej wartości
  # otwarcie bazy danych i odczytanie danej komórki w bazie
  # w przypadku niepowodzenia wyświetlana jest wiadomość o błędzie
###
def SQLread(l_table = 'PWM', l_uC_id = 'Bb'):
    try:
        l_cnx = mysql.connector.connect(user = 'root',
                                        password = 'antek666',
                                        database = 'zgrzewarka_dane')
        l_mycursor = l_cnx.cursor()
        l_SQLcommand = 'SELECT ' +  l_table + ' FROM parametry WHERE id=' + uC_id[l_uC_id]
        l_mycursor.execute(l_SQLcommand)
        l_SQLdata = l_mycursor.fetchall()
        l_cnx.close()
        return l_SQLdata[0][0]
    except:
        print("! ERROR. Odczyt z bazy danych nieudany")
        return 0

### przygotowanie bazy danych
  # otwarcie bazy danych
  # zerowanie wartości PWM, flagi gotowosci i startu
  # w przypadku niepowodzenia wyświetlana jest wiadomość o błędzie
###
def SQLprepare():
    try:
        #Polaczenie z baza danych
        l_cnx = mysql.connector.connect(user = 'root',
                                        password = 'antek666')
        l_mycursor = l_cnx.cursor()
        l_mycursor.execute("USE zgrzewarka_dane")
        #zerowanie wartosci PWM i zmiennej GOTOWOSCI
        for l_x in uC_id:
            l_SQLcommand = 'UPDATE parametry SET PWM=0, czas = 0, PWM1 = 0, czas1 = 0, GOTOWE=0, START=0 WHERE id=' + uC_id[l_x]
            l_mycursor.execute(l_SQLcommand)
            l_cnx.commit()
        print("# Udane otwarcie bazy danych")
        l_cnx.close()
    except:
        print("! ERROR. Nieudane otwarcie bazy danych")

### wpisanie do wskazanego pliku danej wartości
def wpisz_do_pliku(l_plik = '', l_dane_str = ''):
    path = l_plik
    f = open(path, "a")
    f.write(l_dane_str)
    f.close()

### Funkcja odebrania przebiegow zarejestrowanych przez mikrokontroler
  # tworzenie pliku do którego następnie wpisane zostaną odebrane dane
  # wpisanie do bazy danych informacji o zarejestrowanym przebiegu
  # odbieranie danych z mikrokontrolera
###
def odbierz_przebiegi():
    l_time = 0
    l_time2 = 1
    l_string = ''
    l_kolejnosc = 0
    l_dane1 = 0
    l_dane2 = 0
    l_pomiary = 0
    l_licznik = 0

    l_czas = time.localtime()
    l_data_str = str(l_czas[0]) + '-' + str(l_czas[1]) + '-' + str(l_czas[2])
    #print(data_str)
    l_czas_str = str(l_czas[3]) + '.' + str(l_czas[4]) + '.' + str(l_czas[5])
    l_file_name = "Pomiary/" + l_data_str + '_' + l_czas_str + ".txt"
    f = open(l_file_name, "w")
    wpisz_do_pliku(l_file_name, ('Data: ' + l_data_str + "\nCzas: " + l_czas_str + "\n"))
    f.close()

    l_cnx = mysql.connector.connect(user = 'root',
                                password = 'antek666',
                                database = 'zgrzewarka_dane')
    l_mycursor = l_cnx.cursor()
    l_SQLcommand = "INSERT INTO pomiary VALUES (NULL,'" + l_data_str + "', '"  + l_czas_str +  "','" + l_file_name + "');"
    l_mycursor.execute(l_SQLcommand)
    l_cnx.commit()
    l_cnx.close()

    print("$ Trwa akwizycja danych...")
    
    while(l_time < 1.2):
        if(ser.inWaiting()):
            while(ser.inWaiting()):    
                l_UART = ser.read()
                if l_pomiary == 0:
                    l_string = (l_UART.decode())
                    wpisz_do_pliku(l_file_name, l_string)
                    if(l_UART == b'-'):
                        l_pomiary = 1
                        wpisz_do_pliku(l_file_name, '\nt [ms]; I [A]; U [V]; F [kN]\n')
                    
                elif l_UART != b'\xff':
                    if (l_kolejnosc == 1):
                        l_dane2 = int.from_bytes(l_UART, byteorder = 'big')
                        l_dane = l_dane1 * 255 + l_dane2
                        if (l_licznik == 1):
                            l_string =  str(l_time2/10) + '; ' + str(l_dane)
                        elif (l_licznik == 3):
                            l_string =  '; ' + str(l_dane) + '\n'
                            l_licznik = 0
                        else:
                            l_string =  '; ' + str(l_dane)
                        wpisz_do_pliku(l_file_name, l_string)
                        l_time2 = l_time2 + 1
                        l_kolejnosc = 0
                    else:
                        l_kolejnosc = 1
                        l_dane1 = int.from_bytes(l_UART, byteorder = 'big')
                        l_licznik = l_licznik + 1
                l_time = 0
        else:
            l_time = l_time + 0.0001
            time.sleep(0.0001)
    print("$ Koniec oczekowania na dane. Gotowoc do pracy")
    l_pomiary = 0


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
        if toMe == 2 and (confirmFlag[count] == 1 or confirmFlagSTART == 1):
            if licznikUART < 7:
                tabUART[licznikUART] = dataUART
                licznikUART = licznikUART + 1
                if licznikUART == 7:
                    if  (values[count][2].encode() == tabUART[4] and
                         values[count][1].encode() == tabUART[3] and
                         values[count][0].encode() == tabUART[2]):
                        print(tabUART)
                        print("# Poprawne przyjcie wysłanych danych przez uC")
                        clearUARTbuf()
                        licznikUART = 0
                        toMe = 0
                        confirmFlag[count] = 0
                        
                        count = count + 1
                        if (count == 2):
                            count = 0
                        
                    elif tabUART[4] == b'x' and tabUART[3] == b'x' and tabUART[2] == b'x':
                        send_from = tabUART[5].decode() + tabUART[6].decode()
                        SQLwrite('START', '0', send_from)
                        print("$ POPRAWNY START ZGRZEWARKI " + send_from)

                        odbierz_przebiegi()
                        confirmFlagSTART = 0
                        clearUARTbuf()
                        licznikUART = 0
                        toMe = 0
                    else:
                        print(tabUART)
                        print("! uC odebrał dane błędnie")
                        clearUARTbuf()
                        licznikUART = 0
                        toMe = 0
                        confirmFlag[count] = 0
                        resend[count] = 1
                        SQLwrite('GOTOWE', '0', 'Bb')
            else:
                print("! Odebrano bezsensowne dane")
                clearUARTbuf()
                licznikUART = 0
                toMe = 0
                resend[count] = 1
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

    if (czas - czas1 >= 2) and ((confirmFlag[count] == 1) or (confirmFlagSTART == 1)):
        toMe = 0
        licznikUART = 0
        print("! uC nie odpowiedział")
        if(confirmFlag[count] == 1):
            resend[count] = 1
            confirmFlag[count] = 0
        if(confirmFlagSTART == 1):
            confirmFlagSTART = 0
            resendSTART = 1
            print(confirmFlagSTART)
        czas1 = czas

        

    if (czas - czas2 >= 0.5):
        czas2 = czas
        try:     
            SQLdata = SQLread(checkWhat[count], 'Bb')
            if(count == 0):
                #print("~~~~Count 0~~~~")
                if SQLdata < 10 and SQLdata >= 0:
                    dane = "00" + str(SQLdata)
                elif SQLdata < 100  and SQLdata > 0:
                    dane = "0" + str(SQLdata)
                else:
                    dane = "000"
                    print("! ERROR. Niepoprawny format danych")
                if values[count] != dane  or resend[count] == 1:
                    values[count] = dane
                    daneSTR = "Bb" + values[count] + "00"
                    print("# wysłano do uC PWM: " + daneSTR)
                    ser.write(daneSTR.encode())
                    confirmFlag[count] = 1
                    SQLwrite('GOTOWE', '0', 'Bb')
                    print("# Oczekiwanie na odpowiedź uC")
                    resend[count] = 0
                    czas1 = czas
                else:
                    count = 1
            elif(count == 1):
                #print("~~~~Count 1~~~~")
                if SQLdata < 10 and SQLdata >= 0:
                    dane = "100" + str(SQLdata)
                elif SQLdata < 100  and SQLdata > 0:
                    dane = "10" + str(SQLdata)
                elif SQLdata < 1000  and SQLdata > 0:
                    dane = "1" + str(SQLdata)
                else:
                    dane = "1000"
                    print("! ERROR. Niepoprawny format danych")
                if values[count] != dane  or resend[count] == 1:
                    values[count] = dane
                    daneSTR = "Bb" + values[count] + "0"
                    print("# wysłano do uC CZAS: " + daneSTR)
                    ser.write(daneSTR.encode())
                    confirmFlag[count] = 1
                    SQLwrite('GOTOWE', '0', 'Bb')
                    print("# Oczekiwanie na odpowiedź uC")
                    resend[count] = 0
                    czas1 = czas
                else:
                    count = 0
                
                if (confirmFlag[0] == 0 and confirmFlag[1] == 0 and int(values[0]) > 0 and int(values[1]) > 1000):
                    SQLwrite('GOTOWE', '1' , 'Bb')
                else:
                    SQLwrite('GOTOWE', '0' , 'Bb')
            
            
        except:
            print("! ERROR. Nie wyslano nic do uC")

        if (((SQLread('START', 'Bb') == 1 and SQLread('GOTOWE', 'Bb') == 1) or resendSTART == 1) and
            confirmFlag[count] == 0):
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
