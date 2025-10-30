import sys

ALPHABET_LOWER = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
ALPHABET_UPPER = "АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
MODULE = len(ALPHABET_LOWER)

def gen_caesar_key(date_str):
    shift = 0
    for char in date_str:
        if char.isdigit():
            shift += int(char)
    return shift

def gen_vigenere_key(last_name):
    key = ""
    for char in last_name:
        if char in ALPHABET_LOWER or char in ALPHABET_UPPER:
            key += char
    return key.lower()

def caesar_cipher(text, shift, mode='encrypt'):
    result = ""
    if mode == 'decrypt':
        shift = -shift
    
    for char in text:
        if char in ALPHABET_LOWER:
            idx = ALPHABET_LOWER.find(char)
            new_idx = (idx + shift) % MODULE
            result += ALPHABET_LOWER[new_idx]
        elif char in ALPHABET_UPPER:
            idx = ALPHABET_UPPER.find(char)
            new_idx = (idx + shift) % MODULE
            result += ALPHABET_UPPER[new_idx]
        else:
            result += char
    return result

def vigenere_cipher(text, key, mode='encrypt'):
    result = ""
    key_idx = 0
    key_len = len(key)
    if key_len == 0:
        return text

    for char in text:
        if char in ALPHABET_LOWER:
            p_idx = ALPHABET_LOWER.find(char)
            k_char = key[key_idx % key_len]
            k_idx = ALPHABET_LOWER.find(k_char)
            
            if mode == 'encrypt':
                new_idx = (p_idx + k_idx) % MODULE
            else:
                new_idx = (p_idx - k_idx + MODULE) % MODULE
                
            result += ALPHABET_LOWER[new_idx]
            key_idx += 1
        elif char in ALPHABET_UPPER:
            p_idx = ALPHABET_UPPER.find(char)
            k_char = key[key_idx % key_len]
            k_idx = ALPHABET_LOWER.find(k_char)
            
            if mode == 'encrypt':
                new_idx = (p_idx + k_idx) % MODULE
            else:
                new_idx = (p_idx - k_idx + MODULE) % MODULE
                
            result += ALPHABET_UPPER[new_idx]
            key_idx += 1
        else:
            result += char
    return result

def main():
    text_to_encrypt = "Захист інформації – важлива дисципліна"
    user_date = "25.10.2025"
    user_lastname = "Петренко"

    caesar_shift = gen_caesar_key(user_date)
    vigenere_key = gen_vigenere_key(user_lastname)

    print("--- ВХІДНІ ДАНІ ---")
    print(f"Текст: {text_to_encrypt}")
    print(f"Дата для ключа Цезаря: {user_date}")
    print(f"Прізвище для ключа Віженера: {user_lastname}")
    print("-" * 30)

    print("\n--- ДЕМОНСТРАЦІЯ ШИФРУ ЦЕЗАРЯ ---")
    print(f"Згенерований зсув (2+5+1+0+2+0+2+5): {caesar_shift}")
    caesar_encrypted = caesar_cipher(text_to_encrypt, caesar_shift, 'encrypt')
    print(f"Зашифровано: {caesar_encrypted}")
    caesar_decrypted = caesar_cipher(caesar_encrypted, caesar_shift, 'decrypt')
    print(f"Розшифровано: {caesar_decrypted}")
    print("-" * 30)

    print("\n--- ДЕМОНСТРАЦІЯ ШИФРУ ВІЖЕНЕРА ---")
    print(f"Згенерований ключ: {vigenere_key}")
    vigenere_encrypted = vigenere_cipher(text_to_encrypt, vigenere_key, 'encrypt')
    print(f"Зашифровано: {vigenere_encrypted}")
    vigenere_decrypted = vigenere_cipher(vigenere_encrypted, vigenere_key, 'decrypt')
    print(f"Розшифровано: {vigenere_decrypted}")
    print("-" * 30)

    print("\n--- ПОРІВНЯЛЬНИЙ АНАЛІЗ ---")
    print(f"{'Параметр':<20} | {'Шифр Цезаря':<20} | {'Шифр Віженера':<20}")
    print("-" * 64)
    print(f"{'Довжина результату':<20} | {len(caesar_encrypted):<20} | {len(vigenere_encrypted):<20}")
    print(f"{'Читабельність':<20} | {'Дуже низька':<20} | {'Дуже низька':<20}")
    print(f"{'Складність ключа':<20} | {'Проста (1 число)':<20} | {'Складна (слово)':<20}")
    print("-" * 64)

if __name__ == "__main__":
    main()