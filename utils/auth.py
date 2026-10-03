def login_user(company):
    username = input("Login: ").strip()
    password = input("Hasło: ").strip()

    user = company.login(username, password)
    if not user:
        print("Błędny login lub hasło!")
        return None

    print(f"\nWitaj, {user.username}!")
    return user
