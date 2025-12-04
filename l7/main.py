import time
import os
from cryptography.fernet import Fernet
from stegano import lsb

def create_dummy_files():
    if not os.path.exists("input_image.png"):
        from PIL import Image
        img = Image.new('RGB', (100, 100), color = 'red')
        img.save('input_image.png')
    
    with open("secret_data.txt", "w", encoding="utf-8") as f:
        f.write("Це дуже важливі дані для лабораторної роботи.")

def get_metrics(start_time, file_path, label):
    size = os.path.getsize(file_path)
    print(f"[{label}] Розмір: {size} байт")
    print(f"[{label}] Час виконання: {time.time() - start_time:.4f} сек")

def main():
    create_dummy_files()
    
    key = Fernet.generate_key()
    cipher = Fernet(key)
    
    print("--- ПОЧАТОК ЗАХИСТУ ---")
    start_total = time.time()

    with open("secret_data.txt", "rb") as f:
        original_data = f.read()
    
    start_enc = time.time()
    encrypted_data = cipher.encrypt(original_data)
    get_metrics(start_enc, "secret_data.txt", "Шифрування")

    start_stego = time.time()
    secret_image = lsb.hide("input_image.png", encrypted_data.decode())
    secret_image.save("stego_image.png")
    get_metrics(start_stego, "stego_image.png", "Стеганографія")

    print(f"Загальний час захисту: {time.time() - start_total:.4f} сек")
    
    print("\n--- ДЕМОНСТРАЦІЯ ВІДНОВЛЕННЯ ---")
    
    start_restore = time.time()
    
    extracted_string = lsb.reveal("stego_image.png")
    print(f"Витягнутий шифр: {extracted_string[:20]}...")
    
    decrypted_data = cipher.decrypt(extracted_string.encode())
    
    with open("restored_data.txt", "wb") as f:
        f.write(decrypted_data)
        
    print(f"Час відновлення: {time.time() - start_restore:.4f} сек")
    
    if original_data == decrypted_data:
        print("УСПІХ: Файл відновлено ідентично.")
    else:
        print("ПОМИЛКА: Файли не співпадають.")

if __name__ == "__main__":
    main()