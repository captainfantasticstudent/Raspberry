import time
import serial
import mysql.connector
import RPi.GPIO as GPIO

### podstawowe zmienne programu
end= 0                                          #zmienna oznaczająca warunkowe zatrzymanie programu
tab_UART = ['0', '0', '0', '0', '0', '0', '0']  #tablica/lista danych z portu UART
licznik_UART = 0                                #zmienna ilości znaków przechwyconych z portu UART
toMe = 0                                        #czy identyfikator wiadomości do mnie 
confirm_need_START = 0                          #flaga żądzania potwierdzenia
resend_START = 0                                #flaga powtórzenia wysłania wiadomości
ready = 0                                       #flaga gotowości programu

### zmienne potrzebne do ustawienia odpowiednich wartoci w mikrokontrolerze
values = ['-', '-', '-', '-', '-', '-']              #val[0] -> PWM, val[1] -> czas, ...
resend = [0, 0, 0, 0, 0, 0]                        #resend[0] -> PWM, resend[1] -> czas, ...
confirm_need = [0, 0, 0, 0, 0, 0]                  #cf[0] -> PWM, cf[1] -> czas, ...
check_what = ['PWM', 'czas', 'PWM1', 'czas1' , 'MaxI', 'czas_z']     #co należy sprawdzic w bazie danych
count = 0                                       #licznik
SQLdata = 0                                     #dane odczytane z bazy danych
liczba_parametrow = 6                           #stała wykorzystywana dalej w programie

### zmienne potrzebne w wypadku kontroli wicej niż jednego mikrokontrolera zgrzewarki
uC_id = {"Bb":'1'}                              #id mikrokontrolera
uC_list = ["Bb"]                                #lista mikrokontrolerów w sieci
uC_numbers_of = 1                               #liczba mikrokontrolerów w sieci
uC_counter = 0                                  #licznik kolejności obsługi mikrokontrolerów

### zmienne potrzebne do kontorli programu w funkcji czasu
czas = 0                                        #czas który upłynął                                
czasH = 0                                       #liczba godzin która upłynęła
czas1 = 0                                       #zmienna kolejności czasowej
czas2 = 0                                       #zmienna kolejności czasowej

#konfiguracja wyj GPIO
LED1 = 4
LED2 = 3
RxTx = 2
GPIO.setmode(GPIO.BCM)          #Schemat oznacze BCM
GPIO.setwarnings(False)         #Wylaczenie ostrzezeń
GPIO.setup(LED1, GPIO.OUT)      #Port 4 jako wyjście LED
GPIO.setup(LED2, GPIO.OUT)      #Port 3 jako wyjście LED
GPIO.setup(RxTx, GPIO.OUT)      #Port 2 jako wyjście wyboru RX/TX
GPIO.output(LED1, 0)            #stan niski na porcie 4
GPIO.output(LED2, 0)            #stan niski na porcie 4
GPIO.output(RxTx, 0)            #stan niski na porcie 4

### czyszczenie bufora rejestru UART
def clearUARTbuf():
    while(ser.inWaiting()):
        ser.read()

### wpisanie wartoci (l_wartosc) do danej tabeli (l_table) w bazie danych "zgrzewarka_dane"
  # otwarcie bazy danych i aktualizacja wartości w niej zawartych
  # w przypadku niepowodzenia wyświetlana jest wiadomość o błędzie
###
def SQLwrite(l_cell = 'PWM', l_wartosc = '0', l_uC_id = 'Bb'):
    try:
        if(l_cell == 'GOTOWE' and l_wartosc == '0'):    #jeśli będzie zgłaszana niegotowość
            GPIO.output(LED1, 0)                           #dioda gotowości OFF
        #tworzenie połączenia z bazą danych
        l_cnx = mysql.connector.connect(user = 'root',
                                        password = 'antek666',
                                        database = 'zgrzewarka_dane')
        l_mycursor = l_cnx.cursor()         #tworzenie kursora (jest to zbiór rekordów na których
                                            #wykonuje się operacje)
        #komenda SQL uaktualniająca daną komórkę tabeli
        l_SQLcommand = 'UPDATE parametry SET ' + l_cell + '=' + l_wartosc + ' WHERE id=1'
        l_mycursor.execute(l_SQLcommand)    #użycie kwerendy SQL do wprowadzenia zmian w kursorze
        l_cnx.commit()                      #aktualizacja bazy danych przy pomocy kursora
        l_cnx.close()                       #zamykanie połącznia z bazą danych
        return l_wartosc
    except:
        print("! ERROR. Nieudane wpisanie wartosci do bazy danych!")
        return l_wartosc

### odczytanie wartości tabeli (l_table) z bazy i zwrot jej wartości
  # otwarcie bazy danych i odczytanie danej komórki w bazie
  # w przypadku niepowodzenia wyświetlana jest wiadomość o błędzie
###
def SQLread(l_cell = 'PWM', l_uC_id = 'Bb'):
    try:
        #tworzenie połączenia z bazą danych
        l_cnx = mysql.connector.connect(user = 'root',
                                        password = 'antek666',
                                        database = 'zgrzewarka_dane')
        l_mycursor = l_cnx.cursor()         #tworzenie kursora
        #komenda SQL odczytująca wartość komórki z bazy danych
        l_SQLcommand = 'SELECT ' +  l_cell + ' FROM parametry WHERE id=1'
        l_mycursor.execute(l_SQLcommand)    #użycie kwerendy
        l_SQLdata = l_mycursor.fetchall()   #odczyt inforamcji zwrotnej z bazy danych
        l_cnx.close()                       #zamknięcie bazy danych
        return l_SQLdata[0][0]              #zwrot elementu odczytanego z bazy danych
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
        #for l_x in uC_id:
        #    l_SQLcommand = 'UPDATE parametry SET PWM=0, czas = 0, PWM1 = 0, czas1 = 0, MaxI = 0, GOTOWE=0, START=0 WHERE id=' + uC_id[l_x]
        #    l_mycursor.execute(l_SQLcommand)
        #    l_cnx.commit()
        l_SQLcommand = 'UPDATE parametry SET PWM=0, czas = 0, PWM1 = 0, czas1 = 0, MaxI = 0, czas_z = 0, GOTOWE=0, START=0 WHERE id=1'
        l_mycursor.execute(l_SQLcommand)
        l_cnx.commit()
        print("# Udane otwarcie bazy danych")
        l_cnx.close()
    except:
        print("! ERROR. Nieudane otwarcie bazy danych")

### wpisanie do wskazanego pliku danej wartości
def wpisz_do_pliku(l_plik = '', l_dane_str = ''):
    path = l_plik               #tworzenie ścieżki do pliku
    f = open(path, "a")         #otwarcie pliku w trybie dopisywania wartości
    f.write(l_dane_str)         #wpisanie danych do pliku
    f.close()                   #zamknięcie pliku

### Funkcja odebrania przebiegow zarejestrowanych przez mikrokontroler
  # tworzenie pliku do którego następnie wpisane zostaną odebrane dane
  # wpisanie do bazy danych informacji o zarejestrowanym przebiegu
  # odbieranie danych z mikrokontrolera
###
def odbierz_przebiegi():
    #zmienne niezbędne do działania funkcji
    l_time = 0                  #zmienna odliczająca czas
    l_time2 = 1                 #zmnienna określająca czy osiągnięto max czas
    l_string = ''               #zmienna tekstowa wpisywana do bezpośrednio pliku
    l_kolejnosc = 0             #kolejność odbieranych danych z uC
    l_dane1 = 0                 #pierwsza z odbieranych danych z uC
    l_dane2 = 0                 #druga z odbieranych danych z uC
    l_pomiary = 0               #zmienna określająca czy odbierane dane to pomiary czy dane opisowe
    l_licznik = 0               #licznik kolejności wpisywania danych do pliku    
    l_czas = time.localtime()   #dokładny czas i data odbierania pomiaru
    l_czas2 = ['', '', '', '', '', '']  #tablica przechowująca dane string o dacie i czasie pomiaru

    GPIO.output(LED2, 1)    #DIODA ODBIORU DANYCH on
    GPIO.output(LED1, 0)    #dioda gotowości OFF

    #konwersja daty na interesujący nas łańcuch znaków
    for x in range(6):
        if (l_czas[x] > 9):
            l_czas2[x] = str(l_czas[x])
        else:
            l_czas2[x] = '0' + str(l_czas[x]) #uzupełnienie brakujących zer w napisie
    
    l_data_str = l_czas2[0] + '-' + l_czas2[1] + '-' + l_czas2[2]   #string daty w odpowiednim formacie
    l_czas_str = l_czas2[3] + '.' + l_czas2[4] + '.' + l_czas2[5]   #string czasu w odpowiednim formacie
    l_file_name = "/home/ftpuser/download/" + l_data_str + '_' + l_czas_str + ".txt" #ścieżka do zapisu pliku
    f = open(l_file_name, "a")                                      #otwarcie pliku w trybie dopisywania wartości
    #wpisanie do pliku podstawowych informacji identyfikujących pomiar
    wpisz_do_pliku(l_file_name, ('Data: ' + l_data_str + "\nCzas: " + l_czas_str + "\n"))
    f.close()                                                       #zamknięcie obsługi pliku

    #tworzenie połącznia z bazą danych
    l_cnx = mysql.connector.connect(user = 'root',
                                password = 'antek666',
                                database = 'zgrzewarka_dane')
    l_mycursor = l_cnx.cursor() #stworzenie kursora na którycm wykonywane będą operacje na bazie danych
    #komenda wpisania do bazy danych nawej tabeli z danymi o pliku z pomiarami
    l_SQLcommand = "INSERT INTO pomiary VALUES (NULL,'" + l_data_str + "', '"  + l_czas_str +  "','" + l_file_name + "');"
    l_mycursor.execute(l_SQLcommand)    #wykonanie operacji na kursorze
    l_cnx.commit()                      #aktualizacja bazy danych za pomocą kursora
    l_cnx.close()                       #zamknięcie bazy danych

    SQLwrite('GOTOWE', '0', 'Bb')       #zerowanie w bazie danych komórki z flagą gotowości
    ready = 0                           #flaga gotowości programu wyzerowana

    print("$ Trwa akwizycja danych...") #informacja o rozpoczęciu akwizycji danych z bazy

    #jeśli maksymalny czas oczekiwania na dane z mikrokontrolera nie przekroczony
    while(l_time < 1.2):
        if(ser.inWaiting()):                                #jeśli są dane czakające na odczyt z UART
            while(ser.inWaiting()):                         #gdy są dane czakające na odczyt z UART
                l_UART = ser.read()
                if l_pomiary == 0:                          #jeśli informacje opisowe a nie pomiary
                    l_string = (l_UART.decode())            #odczyt bajtu danych i zapis do pliku
                    wpisz_do_pliku(l_file_name, l_string)
                    #jeśli odczytany bajt to sygnał rozpoczęcia nadawania danych pomiarowych
                    if(l_UART == b'-'):                     
                        l_pomiary = 1                       #następne bajty będą danymi pomiarowymi
                        #wpis do pliku informacji o rodzaju i kolejności odebranych danych pomiarowych
                        wpisz_do_pliku(l_file_name, '\nt [ms]; I [A]; U [V]; F [kN]\n')
                    
                elif l_UART != b'\xff' and l_pomiary == 1:   #jeśli dane pomiarowe i otrzymane dane nie błędne             
                    if (l_kolejnosc == 1):                  #jeśli drugi bajt składający się na jedną wartość 16 bitową
                        l_dane2 = int.from_bytes(l_UART, byteorder = 'big') #konwersja i nliczbę
                        l_dane = l_dane1 * 255 + l_dane2                    #tworzenie jednej zmiennej 16 bitowej
                        if (l_licznik == 1):                                #jeśli pierwsza liczba pomiarowa
                            l_string =  str(l_time2/10) + '; ' + str(l_dane)
                        elif (l_licznik == 3):                              #jeśli OSTATNIA liczba pomiarowa
                            l_string =  '; ' + str(l_dane) + '\n'
                            l_licznik = 0
                        else:                                               #w innym przypadku
                            l_string =  '; ' + str(l_dane)
                            l_time2 = l_time2 + 1
                        wpisz_do_pliku(l_file_name, l_string)
                        l_kolejnosc = 0
                    else:                                                   #jeśli pierwsyz bajt zmiennej 16 bitowej
                        l_kolejnosc = 1
                        l_dane1 = int.from_bytes(l_UART, byteorder = 'big')
                        l_licznik = l_licznik + 1
                l_time = 0                                                  #czas oczekiwania zerowany
        else:                           #jeśli brak danych do odebrania łączny czas oczekiwania zwiększany
            l_time = l_time + 0.0001    #czas oczekiwania zwiekszany
            time.sleep(0.0001)          #oczekiwanie 0,1ms
    print("$ Koniec oczekowania na dane. Gotowoc do pracy") #informacja zwrotna
    l_pomiary = 0
    GPIO.output(LED2, 0)    #dioda odbioru danych OFF


### MAIN PROGRAM
  # odczyt i obsługa bazy danych
  # wysylanie wypelnienia PWM poprzez USART
  # sprawdzanie poprawności danych
### END

try:                                    #spróbuj otworzyc interfejs UART
    ser = serial.Serial("/dev/ttyUSB0")	#Przypisanie przejściówki UART podłączonej do wejścia USB (lista urządzeń komendą "dmesg | grep tty" bądź "ls -l dev/")
    ser.baundrate = 9600                        #prędkośc transmisji danych
    ser.timeout = 0
    print("# Konfiguracja USBtty poprawna")
    print("# Port USBtty:" + ser.name)
except:                                 #jeśli się nie udało skończ program i wyświetl info
    print("! Konfiguracja USBtty nieudana, sprawdź ustawienia")
    print("! numer portu USBtty prawdopodobnie sie nie zgadza")
    end = 1

def send_data(l_dane = "00000"):
    GPIO.output(RxTx, 1)        #stan nadawania
    ser.write(l_dane.encode())  #wyslij dane
    while(ser.out_waiting):
        time.sleep(0.000001)
    time.sleep(0.001)
    GPIO.output(RxTx, 0)        #stan odbierania

SQLprepare()    #wyzerowanie bazy danych

print("$ press ENTER to continue")
#input()
print("")

while(end == 0):                                                        #jesli inicjalizacja interfejsu UART udana
    #sprawdzanie czy przyszły dane zwrotne w odpowiedzi na dane wyslane do mikrokontrolera
    while(ser.inWaiting()):                                             #jeśli są dane do odczytu z UART
        dataUART = ser.read()                                           #odczytaj jeden bajt danych
        #jesli dane skierowane do mnie i dane oczekiwane dla danego parametru (flaga żądania potwierdzenia)
        if toMe == 2 and (confirm_need[count] == 1 or confirm_need_START == 1): 
            tab_UART[licznik_UART] = dataUART                       #wpisz dane do tablicy UART
            licznik_UART = licznik_UART + 1                         #inkrementacja licznika odebranych danych
            
            if licznik_UART == 7:                                   #jeśli odebrano 7 bajdów tanych
                #sprawdź czy odebrane dane są TAKIE SAME jak dane wysłane do mikrokontrolera
                if (values[count][4].encode() == tab_UART[6] and
                    values[count][3].encode() == tab_UART[5] and
                    values[count][2].encode() == tab_UART[4] and    
                    values[count][1].encode() == tab_UART[3] and
                    values[count][0].encode() == tab_UART[2]):
                    print(tab_UART)                                 #wypisz odebrane dane
                    print("# Poprawne przyjcie wysłanych danych przez uC")  #podaj info o poprawności odbioru
                    clearUARTbuf()                                  #profilaktycznie wyczyść bufor danych
                    licznik_UART = 0                                #zerój licznik bajtów odebranych
                    toMe = 0                                        #zerój zmienną mówiącą o wiadomości skierowanej do mnie
                    confirm_need[count] = 0                         #zerój flagę żądania potwierdzenia
                    count = count + 1                               #sprawdź następny parametr w głównym programie
                    if (count == liczba_parametrow):                #jeśli to ostatni parametr zacznij od początku
                        count = 0
                #jeśli odebrana wiadomość to wiadmomość startu zgrzewarki
                elif tab_UART[4] == b'x' and tab_UART[3] == b'x' and tab_UART[2] == b'x':
                    send_from = tab_UART[5].decode() + tab_UART[6].decode()     #od jakiego uC odebrano
                    SQLwrite('START', '0', 'Bb')                           #flaga START zerowana w bazie
                    print("$ POPRAWNY START ZGRZEWARKI " + send_from)           #potwierdzenie startu zgrzewarki
                    odbierz_przebiegi()                                         #przygotuj się do odbioru danych pomiarowych
                    confirm_need_START = 0                                      #zerój flagę żądania potwierdzenia startu
                    clearUARTbuf()                                              #profilaktycznie wyczyść bufor danych
                    licznik_UART = 0                                            #zerój licznik bajtów odebranych
                    toMe = 0                                        #zerój zmienną mówiącą o wiadomości skierowanej do mnie

                elif tab_UART[4] == b'z' and tab_UART[3] == b'z' and tab_UART[2] == b'z':
                    SQLwrite('START', '0', 'Bb')                           #flaga START zerowana w bazie
                    print("$ REINICJALIZACJA ZGRZEWARKI")           #potwierdzenie startu zgrzewarki
                    for x in range(liczba_parametrow):
                        resend(x) = 1
                    clearUARTbuf()                                              #profilaktycznie wyczyść bufor danych
                    licznik_UART = 0                                            #zerój licznik bajtów odebranych
                    toMe = 0                                        #zerój zmienną mówiącą o wiadomości skierowanej do mnie
                else:                                   #jeśli dane do niczego nie pasują
                    print(tab_UART)                     #wypisz odebrane błędnie dane
                    print("! uC odebrał dane błędnie")  #info o źle odebranych danych
                    clearUARTbuf()                      #profilaktycznie wyczyść bufor danych
                    licznik_UART = 0                    #zerój licznik bajtów odebranych
                    toMe = 0                            #zerój zmienną mówiącą o wiadomości skierowanej do mnie
                    confirm_need[count] = 0             #zerój flagę żądania potwierdzenia w celu ponownego wysłania danych
                    resend[count] = 1                   #ustaw flagę ponownego wysłania wiadomości
                    SQLwrite('GOTOWE', '0', 'Bb')       #Zerowanie omórki GOTOWOŚCI w bazie danych
                    ready = 0
        else:                                               #czydane skierowane do mnie?
            if licznik_UART == 0 and dataUART == b'C':      #Jeśli odebrany bit to PIERWSZA litera adresu komputera SBC
                toMe = 1                                    #flaga do mnie równa 1
                tab_UART[licznik_UART] = dataUART           #wpisz dane do tablicy UART
                licznik_UART = licznik_UART + 1             #inkrementacja licznika odebranych danych
            elif toMe == 1 and dataUART == b'c':            #Jeśli odebrany bit to DRUGA litera adresu komputera SBC
                toMe = 2                                    #flaga do mnie równa 2 - DANE SKIEROWANE DO KOMPUTERA SBC
                tab_UART[licznik_UART] = dataUART
                licznik_UART = licznik_UART + 1
            else:
                toMe = 0                                    #jeśli identyfikator nierozpoznawany
                licznik_UART = 0                            #zerój licznik bajtów odebranych

    #jeśli czas przewidziany na odpowiedź uC minął i flaka żądania potwierdzenia dla danego parametru ustawiona
    if (czas - czas1 >= 2) and ((confirm_need[count] == 1) or (confirm_need_START == 1)):
        toMe = 0                        #flaga danych do mnie profilaktycznie zerowana
        licznik_UART = 0                #zerój profilaktycznie licznik bajtów odebranych
        print("! uC nie odpowiedział")  #info o nie odesłąniu danych zwrotnych
        if(confirm_need[count] == 1):   #jeśli ustawiona flaga rządania potwierdzenia dla PARAMETRU zgrzewania
            resend[count] = 1           #ustaw flagę ponownego wysłania wiadomości
            confirm_need[count] = 0     #zerój flagę żądania potwierdzenia w celu ponownego wysłania danych
        if(confirm_need_START == 1):    #jeśli ustawiona flaga rządania potwierdzenia dla STARTU zgrzewania
            confirm_need_START = 0
            resend_START = 1
        czas1 = czas                    #wyrównanie czasu w celu odliczania od nowa różnicy

        
    #jeśli nie wymagane potwierdzenie odbioru przez uC (confirm_need[count] == 0) i minął oczekiwany czas sprawdź
    #czy komórki w bazie danych nie zostały zaktualizowane
    if (czas - czas2 >= 0.2 and confirm_need[count] == 0):
        czas2 = czas                                            #wyrównanie czasu w celu odliczania od nowa różnicy
        try:                                                    #spróbuj odczytać wartości z bazy danych
            SQLdata = SQLread(check_what[count], 'Bb')          #odczytaj z bazy danych wartość parametru o danym numerze
            #następnie wykonana akcja zależy od numeru parametru który został odczytany z bazy
            #ciągi danych wysyłanych do uC zaczynają się od numeru ID odbiorcy a potem od numeru parametru którego dotyczy info
            #po numerze odebranego parametru rozpoznawana jest i podejmowana określona akcja na uC
            if(count == 0):                                     #jeśli do sprawdzenia parametr 0 ->PWM
                #print("~~~~Count 0~~~~")
                if SQLdata < 10 and SQLdata >= 0:               #formatowanie odpowiednio odczytanych danych  w łańcuchy string
                    dane = "000" + str(SQLdata) + "0"
                elif SQLdata < 100  and SQLdata > 0:
                    dane = "00" + str(SQLdata) + "0"
                else:
                    dane = "00000"
                    print("! ERROR. Niepoprawny format danych") #info o tym że dane niepoerawne
            elif(count == 1):
                #print("~~~~Count 1~~~~")                       #Sytuacja tego samego typu co powyżej
                if SQLdata < 10 and SQLdata >= 0:               #jedyną różnicą przedrostek liczbowy w wiadomości
                    dane = "100" + str(SQLdata) + "0"
                elif SQLdata < 100  and SQLdata > 0:
                    dane = "10" + str(SQLdata) + "0"
                elif SQLdata < 1000  and SQLdata > 0:
                    dane = "1" + str(SQLdata) + "0"
                else:
                    dane = "10000"
                    print("! ERROR. Niepoprawny format danych")
            elif(count == 2):
                #print("~~~~Count 2~~~~")
                if SQLdata < 10 and SQLdata >= 0:
                    dane = "200" + str(SQLdata) + "0"
                elif SQLdata < 100  and SQLdata > 0:
                    dane = "20" + str(SQLdata) + "0"
                else:
                    dane = "20000"
                    print("! ERROR. Niepoprawny format danych")
            elif(count == 3):
                #print("~~~~Count 3~~~~")
                if SQLdata < 10 and SQLdata >= 0:
                    dane = "300" + str(SQLdata) + "0"
                elif SQLdata < 100  and SQLdata > 0:
                    dane = "30" + str(SQLdata) + "0"
                elif SQLdata < 1000  and SQLdata > 0:
                    dane = "3" + str(SQLdata) + "0"
                else:
                    dane = "30000"
                    print("! ERROR. Niepoprawny format danych")
            elif(count == 4):
                #print("~~~~Count 4~~~~")
                if SQLdata < 10 and SQLdata >= 0:
                    dane = "400" + str(SQLdata) + "0"
                elif SQLdata < 100  and SQLdata > 0:
                    dane = "40" + str(SQLdata) + "0"
                elif SQLdata < 1000  and SQLdata > 0:
                    dane = "4" + str(SQLdata) + "0"
                else:
                    dane = "40000"
                    print("! ERROR. Niepoprawny format danych")
            elif(count == 5):
                #print("~~~~Count 4~~~~")
                if SQLdata < 10 and SQLdata >= 0:
                    dane = "500" + str(SQLdata) + "0"
                elif SQLdata < 100  and SQLdata > 0:
                    dane = "50" + str(SQLdata) + "0"
                elif SQLdata < 1000  and SQLdata > 0:
                    dane = "5" + str(SQLdata) + "0"
                else:
                    dane = "50000"
                    print("! ERROR. Niepoprawny format danych")
            
            if values[count] != dane  or resend[count] == 1:    #jeśli dane z BAZY != ostatnio wysłane dane lub resend wyślij dane
                values[count] = dane                            #zapisanie w pamięciu nowej wartości 
                daneSTR = "Bb" + values[count]                  #utwórz odpowiedni łąńcuch
                print("# wysłano do uC sygnał: " + daneSTR)     #info o wysłaniu danych
                send_data(daneSTR)                              #wysyłanie danych przez UART do uC
                confirm_need[count] = 1                         #flaga żądania potwierdzenia
                SQLwrite('GOTOWE', '0', 'Bb')                   #ustawienie niegotowości zgrzewarki
                ready = 0                                       #flaga gotowości zerowana
                print("# Oczekiwanie na odpowiedź uC")          #wiadomość do użytkownika
                resend[count] = 0                               #flaga potrzeby ponownego wysłania zerowana
                czas1 = czas                                    #ustawienie czasu oczekiwania na odpowiedź na odpowiednim poziomie
            else:
                count = count + 1
                if (count == liczba_parametrow):
                    count = 0
                    #sprawczenie czy zgrzewarka jest gotowa oraz czy wpisane do zmiennych wartości są prawidłowe
                    if (confirm_need[0] == 0 and confirm_need[1] == 0 and confirm_need[2] == 0 and confirm_need[3] == 0 and confirm_need[4] == 0 and confirm_need[5] == 0
                        and int(values[0]) > 0 and int(values[1]) > 1000 and int(values[2]) > 1999 and int(values[3]) > 2999 and int(values[4]) > 3999 and int(values[5]) > 4999
                        and ((int(values[3]) > (int(values[1]) + 2000)) or int(values[3]) == 3000)):
                        SQLwrite('GOTOWE', '1' , 'Bb')                          #jeśli tak pisz w bazę danych gotowość
                        GPIO.output(LED1, 1)                                    #dioda gotowości ON
                        if ready == 0:                                          #jeśli flaga gotowości = 0
                            print("$ POTWIERDZENIE GOTOWOSCI ZGRZEWARKI")       #potwierdź gotowość
                            ready = 1                                           #ustaw flagę gotowości
                    else:
                        SQLwrite('GOTOWE', '0' , 'Bb')                          #jeśli jeszcze nie wszystko wpisano/sprawdzono gotowość = 0
                        ready = 0
              
        except:                                                                 #jeśli nieudany odczyt wartości  z bazy danych
            print("! ERROR. Nie wyslano nic do uC")

        #sprawdzanie flagi startu na podobnej zasadzie jak wyżej
        if (((SQLread('START', 'Bb') == 1 and SQLread('GOTOWE', 'Bb') == 1) or resend_START == 1) and
            confirm_need[count] == 0):
            kodPotwierdzenia = 'Bb' + "xxx" + "Cc"  #wyślij do uC kod startu!
            send_data(kodPotwierdzenia)
            confirm_need_START = 1                  #wymagaj potwierdzenia startu uC
            resend_START = 0                        #zerój flagę ponownego wysłąnia
            czas1 = czas                            #dostosuj czas
    
    time.sleep(0.1)     #oczekuj 100ms
    czas = czas + 0.1   #zwiększ czas który upłynął

    if czas == 3600:    #odlicznie czasu
        czasH = 1
        czas = 0
        czas1 = 0
        czas2 = 0

GPIO.cleanup()          #zerój ustawienia GPIO
