# Odczyt i zapis do pliku

plik = open("/home/pi/Desktop/Raspberry/Programy/tekst.txt", 'w')
plik.write("napis\n")
plik.close
print("zapisano tekst do pliku")

plik = open("/home/pi/Desktop/Raspberry/Programy/tekst.txt", 'a')
plik.write("napis2")
plik.close
print("dopisano tekst na końcu pliku")

plik = open("/home/pi/Desktop/Raspberry/Programy/tekst.txt", 'r')
odczytany_tekst = plik.read()
plik.close
print("\nodczytano z pliku:\n" + odczytany_tekst)

