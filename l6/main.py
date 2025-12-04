import sqlite3
import time

def setup_db():
    """Створює базу даних у пам'яті та наповнює її користувачами."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)")
    
    # Додаємо кілька акаунтів
    users = [
        ('admin', 'admin123', 'Administrator'),
        ('alice', 'wonderland', 'User'),
        ('bob', 'builder', 'User'),
        ('eve', 'evil_hacker', 'Banned')
    ]
    cursor.executemany("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", users)
    conn.commit()
    return conn

def unsafe_login(conn, username, password):
    """НЕБЕЗПЕЧНА функція: використовує f-string для формування запиту."""
    cursor = conn.cursor()
    # ВРАЗЛИВІСТЬ ТУТ: пряма вставка змінних у рядок запиту
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    
    print(f"\n[LOG] Виконується SQL (Unsafe): {query}")
    
    try:
        cursor.execute(query)
        user = cursor.fetchone()
        return user
    except sqlite3.Error as e:
        print(f"[ERROR] Помилка SQL: {e}")
        return None

def safe_login(conn, username, password):
    """БЕЗПЕЧНА функція: використовує параметризовані запити."""
    cursor = conn.cursor()
    # БЕЗПЕКА: знаки '?' є плейсхолдерами
    query = "SELECT * FROM users WHERE username=? AND password=?"
    
    print(f"[LOG] Виконується SQL (Safe): {query} з параметрами {(username, password)}")
    
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    return user

def print_result(user, method_name):
    if user:
        print(f"🔓 {method_name}: УСПІХ! Вхід виконано як: {user[1]} (Роль: {user[3]})")
    else:
        print(f"🔒 {method_name}: ВІДМОВА. Невірний логін або пароль.")

def run_scenario(conn, scenario_name, u_input, p_input):
    print(f"\n--- СЦЕНАРІЙ: {scenario_name} ---")
    print(f"Введені дані -> Логін: {u_input} | Пароль: {p_input}")
    
    # 1. Спроба злому через вразливий код
    user_unsafe = unsafe_login(conn, u_input, p_input)
    print_result(user_unsafe, "ВРАЗЛИВИЙ МЕТОД")
    
    # 2. Перевірка захисту
    user_safe = safe_login(conn, u_input, p_input)
    print_result(user_safe, "БЕЗПЕЧНИЙ МЕТОД")

def main():
    conn = setup_db()
    
    while True:
        print("\n" + "="*40)
        print("   СИМУЛЯТОР SQL INJECTION (PYTHON)")
        print("="*40)
        print("1. Ввести логін/пароль вручну (Своя атака)")
        print("2. Демо: Обхід пароля коментарем (-- )")
        print("3. Демо: Логічна ін'єкція (OR 1=1)")
        print("4. Показати всіх користувачів в базі")
        print("0. Вихід")
        
        choice = input("\nОберіть дію: ")
        
        if choice == '1':
            u = input("Введіть username: ")
            p = input("Введіть password: ")
            run_scenario(conn, "Ручне введення", u, p)
            
        elif choice == '2':
            # Атака: закриваємо лапку ' потім ставимо коментар --
            # Все що йде після -- (тобто перевірка пароля) ігнорується базою
            u_payload = "admin' --"
            p_payload = "будь-який_текст" 
            run_scenario(conn, "Коментування запиту (Comment Injection)", u_payload, p_payload)
            
        elif choice == '3':
            # Атака: закриваємо лапку, додаємо умову АБО ІСТИНА
            u_payload = "admin" # або можна ' OR '1'='1
            p_payload = "' OR '1'='1"
            run_scenario(conn, "Логічна тотожність (Tautology)", u_payload, p_payload)

        elif choice == '4':
            cursor = conn.cursor()
            print("\nСписок користувачів у базі:")
            for row in cursor.execute("SELECT * FROM users"):
                print(row)
                
        elif choice == '0':
            print("Вихід...")
            break
        else:
            print("Невірний вибір.")
            
        time.sleep(1)

if __name__ == "__main__":
    main()