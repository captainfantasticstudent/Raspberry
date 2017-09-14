import copy

# LISTY #
lista = [23, 32.5, "napis"]
print(len(lista))

lista[0] = "XXX"

lista.append("ha")
print(lista)

lista.insert(1, 23)
print(lista)

lista2 = [2, 3, 4]
lista.extend(lista2)
print(lista)

lista.pop(3)
print(lista)

print("s-g-f".split('-'))

for x in lista:
    print(x)

for (i, x) in enumerate(lista):
    print(i, " ", x)

lista1 = copy.copy(lista)
print(lista1)

lista3 = ["s", "dsf", "wer"]
lista3.sort()
print(lista3)

lista4 = lista[1:3]
print(lista4)

# ZŁOŻENIA #
[print(x.upper()) for x in lista3]

# SŁOWNIKI #
slownik = {"pierwszy":1, "drugi":2}
print(slownik)

print(slownik["pierwszy"])

for num, x in slownik.items():
    print(num, " ", x)
