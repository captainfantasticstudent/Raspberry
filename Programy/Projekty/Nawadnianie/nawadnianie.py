# Program do nawadniania roślin
import time

def sprawdz_nawodnienie():
    poziom_nawodnienia = 0
    return poziom_nawodnienia
    
def nawodnij():
    try:
        #funkcja włączenia pąpki
        nawodniono = 1
    except:
        #jeśli operacja nieudana
        nawodniono = 0

def zapisz_stan():
    dzien = 0
    nowe_pomiary = 0
    try:
        plik = open("day.txt", "r")
        dzien = int(plik.read())
        dzien = dzien
        print("Dzień pomiarów:", dzien)
        plik.close
    except:
        print("* Nie znaleziono pliku z dniem pomiarów!")
        try:
            plik = open("day.txt", "w")
            print("* Utworzono nowy plik z dniem pomiarów")
            dzien = 1
            plik.write(str(dzien))
            print("Dzień pomiarów:", dzien)
            plik.close()
        except:
            print("Problem ze stworzeniem nowego pliku!")
    try:
        nazwa_pliku = "pomiary_dzień_" + str(dzien) + ".txt"
        plik = open(nazwa_pliku, "a")
        plik.write("POMIAR\n")
        plik.close()
    except:
        print("* Nie udało się otworzyć pliku z danymi!")

while(1):
    zapisz_stan()
    time.sleep(10)
