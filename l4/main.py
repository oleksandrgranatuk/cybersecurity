import hashlib

name = input("Ім'я: ")
dob = input("Дата народження: ")
secret = input("Секретне слово: ")

data = name + dob + secret
private_key = hashlib.sha256(data.encode()).hexdigest()
public_key = hashlib.sha256(private_key.encode()).hexdigest()

with open("private_key.txt", "w") as f:
    f.write(private_key)

with open("public_key.txt", "w") as f:
    f.write(public_key)