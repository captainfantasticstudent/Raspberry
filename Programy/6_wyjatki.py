try:
    print("Import metody")
    import metoda
except ImportError:
    print("Problem z wczytaniem metody (input)")
else:
    print("zaimportowano metodę")
finally:
    print("obsługa wyjątków zakończona")
