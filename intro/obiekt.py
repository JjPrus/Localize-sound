class Osoba:
    """Opis klasy"""
    def __init__(self, imie, nazwisko, wiek):  # konstruktor (przygotowanie miejsca w pamięci)
        self.imie = imie  # tworzymy pole na podstawie wartości podanej w funkcji
        self.nazwisko = nazwisko
        self.wiek = wiek

    def przedstaw_sie(self):
        print('Nazywam się {} {} i mam {} lata'.format(self.imie, self.nazwisko, self.wiek))


Kleofas = Osoba('Kleofas', 'Niemiły', 24)
Kleofas.przedstaw_sie()
Osoba.przedstaw_sie(Kleofas)
print(Kleofas.imie)
print(Kleofas.__dict__)

Kleofas.plec = 'M'
print(Kleofas.__dict__)
