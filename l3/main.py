from PIL import Image
import os

DELIMITER = "||END||"

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary_str):
    text = ""
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i+8]
        if len(byte) < 8:
            break
        text += chr(int(byte, 2))
    return text

def hide_message(image_path, message, output_path):
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    data = img.load()
    
    message_with_delimiter = message + DELIMITER
    binary_message = text_to_binary(message_with_delimiter)
    
    max_bits = width * height * 3
    if len(binary_message) > max_bits:
        raise ValueError("Повідомлення занадто велике для цього зображення")
        
    bit_index = 0
    
    for y in range(height):
        for x in range(width):
            r, g, b = data[x, y]
            
            if bit_index < len(binary_message):
                new_r = (r & ~1) | int(binary_message[bit_index])
                bit_index += 1
            else:
                new_r = r
                
            if bit_index < len(binary_message):
                new_g = (g & ~1) | int(binary_message[bit_index])
                bit_index += 1
            else:
                new_g = g
                
            if bit_index < len(binary_message):
                new_b = (b & ~1) | int(binary_message[bit_index])
                bit_index += 1
            else:
                new_b = b
                
            data[x, y] = (new_r, new_g, new_b)
            
            if bit_index >= len(binary_message):
                break
        if bit_index >= len(binary_message):
            break
            
    img.save(output_path, "PNG")

def extract_message(image_path):
    img = Image.open(image_path).convert("RGB")
    width, height = img.size
    data = img.load()
    
    binary_extracted = ""
    found_message = None
    
    for y in range(height):
        for x in range(width):
            r, g, b = data[x, y]
            
            binary_extracted += str(r & 1)
            binary_extracted += str(g & 1)
            binary_extracted += str(b & 1)
            
            if len(binary_extracted) % 8 == 0 and len(binary_extracted) > len(DELIMITER) * 8:
                text_so_far = binary_to_text(binary_extracted)
                if DELIMITER in text_so_far:
                    found_message = text_so_far.split(DELIMITER)[0]
                    break
        if found_message:
            break
            
    return found_message

if __name__ == "__main__":
    input_image = "photo1.png"
    output_image = "stego_image.png"
    
    my_personal_data = "My name is Oleksandr Granatuk. My email is: oleksandrgranatuk496@gmail.com. Password: MySecretPassword123."

    try:
        if not os.path.exists(input_image):
            raise FileNotFoundError(f"Файл не знайдено: {input_image}. Будь ласка, переконайтеся, що файл існує, і ви правильно вказали ім'я.")

        original_size = os.path.getsize(input_image)
        print(f"Використовуємо зображення: {input_image}")
        print(f"Початковий розмір файлу: {original_size} байт")
        
        print("\n--- Демонстрація роботи ---")
        print(f"Приховуємо повідомлення: '{my_personal_data}'")
        
        hide_message(input_image, my_personal_data, output_image)
        print(f"Повідомлення приховано. Змінене зображення збережено як: {output_image}")
        
        print("\nВитягуємо повідомлення для перевірки...")
        extracted_data = extract_message(output_image)
        
        if extracted_data:
            print(f"Витягнуте повідомлення: '{extracted_data}'")
        else:
            print("Не вдалося знайти повідомлення.")
            
        if extracted_data == my_personal_data:
            print("\nВерифікація успішна: витягнуті дані збігаються з оригіналом.")
        else:
            print("\nПомилка верифікації!")
            
        print("\n--- Аналіз змін (Практичний) ---")
        stego_size = os.path.getsize(output_image)
        print(f"Новий розмір файлу: {stego_size} байт")
        print(f"Різниця в розмірі: {stego_size - original_size} байт")
        
        print(f"\nОригінал '{input_image}' та змінений файл '{output_image}' збережено.")

    except FileNotFoundError as e:
        print(f"\nПОМИЛКА: {e}")
    except Exception as e:
        print(f"\nСталася неочікувана помилка: {e}")

