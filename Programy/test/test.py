# PROGRAM NAPISANY DLA TESTÓW #

# zapis danych godziny i temperatury do pliku
import random

while True:
    dane = open("/home/pi/Desktop/Raspberry/Programy/test/temp.txt", 'w')
    roznica = 2
    for x in range(8, 21):
        if(x > 8):
            temperatura_poprzednia = temperatura
        temperatura = random.randint(10, 29) + random.random()
        if(x == 8):
            temperatura_poprzednia = temperatura

        if((temperatura_poprzednia - temperatura) > roznica and temperatura_poprzednia > 10+roznica):
            temperatura = temperatura_poprzednia - roznica    
        elif((temperatura_poprzednia - temperatura) > roznica and temperatura_poprzednia < 10+roznica):
            temperatura = 10
        elif((temperatura_poprzednia - temperatura) < -roznica and temperatura_poprzednia < 30-roznica):
            temperatura = temperatura_poprzednia + roznica
        elif((temperatura_poprzednia - temperatura) > roznica and temperatura_poprzednia > 30-roznica):
            temperatura = 30
            
        dane.write(str(x) + ":00," + "{:.2f}".format(temperatura))   
        if(x < 20):
            dane.write("\n")
    dane.close()


    # odczyt danych temperatury z pliku
    dane = open("/home/pi/Desktop/Raspberry/Programy/test/temp.txt", 'r')

    tresc_danych = dane.read().split("\n")

    for x in tresc_danych:
        dane_temperatur = x.split(',')
        godzina = dane_temperatur[0]
        temperatura = dane_temperatur[1]
        y = 0
        slupek = ''
        while y < float(temperatura):
            slupek = slupek + "@"
            y = y + 1
        while y < 32:
            slupek = slupek + " "
            y = y + 1
        print(slupek + "godzina: " + godzina + "\ttemperatura: " + temperatura)
    dane.close()
    input()
