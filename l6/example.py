import sqlite3

def run_demo():
    # 1. Налаштування бази даних (створення в пам'яті)
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    
    # Створюємо таблицю користувачів і додаємо адміністратора
    cursor.execute("CREATE TABLE users (username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users VALUES ('admin', 'SuperSecretPass123')")
    connection.commit()

    print("--- БАЗА ДАНИХ НАЛАШТОВАНА ---")
    print("В базі є користувач: admin з паролем: SuperSecretPass123\n")

    # 2. Вхідні дані від "хакера"
    input_user = "admin'--"
    input_pass = "123" 

    print(f"Введені дані користувача: {input_user}")
    print(f"Введений пароль (атака):   {input_pass}\n")

    # ==========================================
    # СЦЕНАРІЙ 1: НЕБЕЗПЕЧНИЙ (String Formatting)
    # ==========================================
    print(">>> СПРОБА 1: НЕБЕЗПЕЧНИЙ ЗАПИТ (f-string)")
    
    # Тут ми просто вклеюємо текст у запит. Це помилка!
    unsafe_query = f"SELECT * FROM users WHERE username='{input_user}' AND password='{input_pass}'"
    
    print(f"Сформований SQL: {unsafe_query}")
    
    cursor.execute(unsafe_query)
    result = cursor.fetchone()
    
    if result:
        print("🔴 РЕЗУЛЬТАТ: УСПІХ! Вхід виконано (Атака спрацювала).")
        print(f"   Ми отримали дані: {result}")
    else:
        print("🟢 РЕЗУЛЬТАТ: ВІДМОВА.")

    print("-" * 40 + "\n")

    # ==========================================
    # СЦЕНАРІЙ 2: БЕЗПЕЧНИЙ (Parameterized Query)
    # ==========================================
    print(">>> СПРОБА 2: БЕЗПЕЧНИЙ ЗАПИТ (Placeholders)")
    
    # Використовуємо знаки питання як плейсхолдери
    safe_query = "SELECT * FROM users WHERE username=? AND password=?"
    
    # Передаємо дані окремим кортежем (tuple)
    # База даних сприйме input_pass як звичайний текст, а не як команду
    cursor.execute(safe_query, (input_user, input_pass))
    result = cursor.fetchone()
    
    if result:
        print("🔴 РЕЗУЛЬТАТ: УСПІХ! (Це погано, якщо атака пройшла).")
    else:
        print("🟢 РЕЗУЛЬТАТ: ВІДМОВА! Вхід заблоковано (Атака не пройшла).")

    connection.close()

if __name__ == "__main__":
    run_demo()