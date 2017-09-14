class Car:
    "Klasa bazowa samochodu"
    def __init__(self, color):
        self.wheels = ["PP", "LP", "PT", "LT"]
        self.engine = 1500
        self.colour = color
    def change_color(self, color):
        self.color = color
        print("zmieniono na: ", self.color)

class Marka(Car):
    "Samochód danej marki i koloru"
    def __init__(self, marka, kolor):
        Car.__init__(self, kolor)
        self.marka = marka
        print("Wybrano", kolor, self.marka)
    def zmien_marke(self, marka):
        self.marka = marka
        print("zmieniono na: ", self.marka)
