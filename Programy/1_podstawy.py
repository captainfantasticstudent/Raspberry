import random

# Definicja funkcji #
def liczba_losowa(a = 0, b = 10):
    liczba = random.randint(a, b-1) + random.random()
    return liczba

# Pierwsza część #
print("# Pierwsza część #")
for i in range(0, 11):
    x = liczba_losowa(0, 10)
    if i % 2 == 0:
        print(str(i) + '. ' + "liczba x: " + str(x))

if (x > 7):
    print("Liczba większa od 7, liczba: ", x)
elif (x > 3):
    print("Liczba większa od 3 i mniejsza od 7, liczba: ", x)
else:
    print("liczba mniejsza od 3, liczba: ", x)

# Druga część #
print("\n# Druga część #")
y = liczba_losowa(0, 12)
while (y < 8):
    y = liczba_losowa(0, 12)
    print("y mniejsze od 8")
print("y równe: ", y)

# Trzecia część #
print("\n# Trzecia część #")
n = "Program pisany w "
n = n + str(2017) + " roku"
print(n)
n = input("Wpisz tekst: ")
print("Wpisany tekst:", n, ", Długość wpisanego tekstu:", len(n))


