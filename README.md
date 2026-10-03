# Projekt: System zarządzania firmą

To jest projekt na zaliczenie z informatyki w Pythonie. Program działa w trybie konsolowym i zapisuje dane w formacie JSON.

## Co zawiera projekt
- logowanie użytkowników jako admin lub pracownik
- oddzielne klasy w osobnych plikach
- dziedziczenie (Admin, Employee -> User)
- kompozycja (firma, pracownicy, produkty, zamówienia)
- minimum 3 produkty dostępne do sprzedaży
- finanse firmy zapisane w JSON
- raport tekstowy z aktualnymi danymi o firmie

## Struktura projektu
- `classes/` – klasy modelowe
- `data/` – pliki JSON z danymi
- `utils/` – obsługa JSON i logowania
- `main.py` – menu główne programu

## Uruchomienie
```bash
python main.py
```

## Domyślni użytkownicy
- admin / admin123
- manager / manager123
- seller / seller123

## Wymagania
- Python 3.x
- brak dodatkowych bibliotek
