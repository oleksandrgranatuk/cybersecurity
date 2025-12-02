import hashlib
import base64

email = input("Введіть email: ")
key_data = input("Введіть дані для генерації ключа: ")
text = input("Введіть повідомлення: ")

key_hash = hashlib.sha256(key_data.encode()).digest()

text_bytes = text.encode()
encrypted_bytes = bytearray()

for i in range(len(text_bytes)):
    encrypted_bytes.append(text_bytes[i] ^ key_hash[i % len(key_hash)])

encrypted_result = base64.b64encode(encrypted_bytes).decode()

print(f"\n--- Результат ---")
print(f"Email: {email}")
print(f"Згенерований ключ (hex): {key_hash.hex()}")
print(f"Зашифровані дані: {encrypted_result}")

decrypted_bytes = bytearray()
raw_encrypted = base64.b64decode(encrypted_result)

for i in range(len(raw_encrypted)):
    decrypted_bytes.append(raw_encrypted[i] ^ key_hash[i % len(key_hash)])

print(f"Розшифроване повідомлення: {decrypted_bytes.decode()}")