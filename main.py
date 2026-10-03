from classes.company import Company
from classes.admin import Admin
from classes.employee import Employee
from classes.product import Product
from utils.auth import login_user


def show_products(company):
    print("\n=== PRODUKTY ===")
    if not company.products:
        print("Brak produktów.")
        return

    for product in company.products:
        print(f"- {product.name} | Cena: {product.price} zł | Ilość: {product.stock} | Kategoria: {product.category}")


def admin_menu(company):
    while True:
        print("\n=== PANEL ADMINA ===")
        print("1. Pokaż użytkowników")
        print("2. Dodaj nowego użytkownika")
        print("3. Zmień dane użytkownika")
        print("4. Pokaż produkty")
        print("5. Dodaj produkt")
        print("6. Sprzedaj produkt")
        print("7. Generuj raport")
        print("8. Wyloguj")

        choice = input("Wybór: ").strip()

        if choice == "1":
            print("\nUŻYTKOWNICY:")
            for user in company.users:
                print(f"- {user.username} | Rola: {user.role} | Stanowisko: {user.position} | Uprawnienia: {', '.join(user.permissions)}")

        elif choice == "2":
            username = input("Nazwa użytkownika: ").strip()
            password = input("Hasło: ").strip()
            role = input("Rola (admin/employee): ").strip().lower()
            position = input("Stanowisko: ").strip()
            salary = float(input("Pensja: ").strip() or 0)

            if role == "admin":
                user = Admin(username, password)
            else:
                user = Employee(username, password, position=position, salary=salary)

            if company.add_user(user):
                print("Dodano użytkownika.")
            else:
                print("Taki użytkownik już istnieje.")

        elif choice == "3":
            username = input("Nazwa użytkownika do zmiany: ").strip()
            user = company.get_user_by_username(username)
            if not user:
                print("Nie znaleziono użytkownika.")
                continue

            new_password = input("Nowe hasło (enter bez zmiany): ").strip()
            new_position = input("Nowe stanowisko (enter bez zmiany): ").strip()
            new_salary = input("Nowa pensja (enter bez zmiany): ").strip()

            changes = {}
            if new_password:
                changes["password"] = new_password
            if new_position:
                changes["position"] = new_position
            if new_salary:
                changes["salary"] = float(new_salary)

            if company.update_user(username, **changes):
                print("Dane użytkownika zostały zaktualizowane.")
            else:
                print("Błąd przy aktualizacji.")

        elif choice == "4":
            show_products(company)

        elif choice == "5":
            name = input("Nazwa produktu: ").strip()
            price = float(input("Cena: ").strip())
            stock = int(input("Ilość na magazynie: ").strip())
            category = input("Kategoria: ").strip() or "Ogólne"

            product = Product(name=name, price=price, stock=stock, category=category)
            company.add_product(product)
            print("Dodano produkt.")

        elif choice == "6":
            product_name = input("Nazwa produktu: ").strip()
            quantity = int(input("Ilość: ").strip())
            employee_name = input("Sprzedawca (login): ").strip()
            customer_name = input("Imię klienta: ").strip() or "Klient"

            result = company.sell_product(product_name, quantity, employee_name, customer_name)
            if result["success"]:
                print(result["message"])
            else:
                print(result["message"])

        elif choice == "7":
            print("\n" + company.generate_report())

        elif choice == "8":
            break

        else:
            print("Nieznana opcja.")


def employee_menu(company, user):
    while True:
        print("\n=== PANEL PRACOWNIKA ===")
        print("1. Pokaż produkty")
        print("2. Sprzedaj produkt")
        print("3. Generuj raport")
        print("4. Wyloguj")

        choice = input("Wybór: ").strip()

        if choice == "1":
            show_products(company)

        elif choice == "2":
            if not user.has_permission("sell") and not user.has_permission("all"):
                print("Brak uprawnień do sprzedaży.")
                continue

            product_name = input("Nazwa produktu: ").strip()
            quantity = int(input("Ilość: ").strip())
            customer_name = input("Imię klienta: ").strip() or "Klient"

            result = company.sell_product(product_name, quantity, user.username, customer_name)
            if result["success"]:
                print(result["message"])
            else:
                print(result["message"])

        elif choice == "3":
            print("\n" + company.generate_report())

        elif choice == "4":
            break

        else:
            print("Nieznana opcja.")


def main():
    company = Company("Firma XYZ")
    print("=== SYSTEM ZARZĄDZANIA FIRMĄ ===")
    print("Domyślni użytkownicy:")
    print("- admin / admin123")
    print("- manager / manager123")
    print("- seller / seller123")

    while True:
        print("\n=== MENU GŁÓWNE ===")
        print("1. Zaloguj się")
        print("2. Zakończ")

        choice = input("Wybór: ").strip()

        if choice == "1":
            user = login_user(company)
            if not user:
                continue

            if user.role == "admin":
                admin_menu(company)
            else:
                employee_menu(company, user)

        elif choice == "2":
            print("Do widzenia!")
            break

        else:
            print("Nieznana opcja.")


if __name__ == "__main__":
    main()
