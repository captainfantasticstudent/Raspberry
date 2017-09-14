# Zrzucanie danych o liście (i nie tylko) do pliku i ponowne ich wczytywanie

import pickle

lista = ['a', 23, 32.4534]
try:
    zmienna_test = 6
    f = open('lista', 'wb')
    pickle.dump(lista, f)
    f.close()
    print("Zapisano listę")
except:
    print("Nieudane zapisanie listy")

try:
    with open("lista", 'rb') as f:
        inna_lista = pickle.load(f)
        print(inna_lista)
        print("Wczytano listę")
except:
    print("Nieudane wczytanie listy")
