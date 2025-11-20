import hashlib

class DigitalSignatureSystem:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def generate_keys(self, surname, birthdate, secret):
        raw_string = f"{surname}{birthdate}{secret}"
        sha_signature = hashlib.sha256(raw_string.encode()).hexdigest()
        self.private_key = int(sha_signature, 16)
        self.public_key = (self.private_key * 7) % 1000007
        return self.private_key, self.public_key

    def get_document_hash(self, content):
        return int(hashlib.sha256(content.encode()).hexdigest(), 16)

    def sign_document(self, content):
        doc_hash = self.get_document_hash(content)
        signature = doc_hash ^ self.private_key
        return signature

    def verify_signature(self, content, signature):
        current_doc_hash = self.get_document_hash(content)
        decrypted_hash = signature ^ self.private_key
        
        if decrypted_hash == current_doc_hash:
            return True
        return False

system = DigitalSignatureSystem()

print("--- 1. ГЕНЕРАЦІЯ КЛЮЧІВ ---")
priv, pub = system.generate_keys("Петренко", "15031995", "secret_word")
print(f"Приватний ключ: {priv}")
print(f"Публічний ключ: {pub}")

print("\n--- 2. ПІДПИСАННЯ ДОКУМЕНТУ ---")
document_content = "Резюме кандидата Петренка: досвід роботи 5 років"
signature = system.sign_document(document_content)
print(f"Вміст документу: {document_content}")
print(f"Цифровий підпис: {signature}")

print("\n--- 3. ПЕРЕВІРКА ОРИГІНАЛЬНОГО ДОКУМЕНТУ ---")
is_valid = system.verify_signature(document_content, signature)
if is_valid:
    print("Результат: Підпис ДІЙСНИЙ")
else:
    print("Результат: Підпис ПІДРОБЛЕНИЙ")

print("\n--- 4. ДЕМОНСТРАЦІЯ ПІДРОБКИ ---")
fake_document = "Резюме кандидата Петренка: досвід роботи 10 років"
print(f"Змінений документ: {fake_document}")
is_valid_fake = system.verify_signature(fake_document, signature)

if is_valid_fake:
    print("Результат: Підпис ДІЙСНИЙ")
else:
    print("Результат: Підпис ПІДРОБЛЕНИЙ")