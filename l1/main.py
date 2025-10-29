import re
import string

def extract_personal_data(name, dob):
    parts = []
    
    name_lower = name.lower()
    parts.append(name_lower)
    
    if name_lower == 'іван':
        parts.append('ivan')
    
    dob_parts = re.findall(r'\d+', dob)
    parts.extend(dob_parts)
    
    for part in dob_parts:
        if len(part) == 4 and part.startswith(('19', '20')):
            parts.append(part[2:])
            
    return [part for part in parts if len(part) > 1]

def analyze_password(password, name, dob):
    score = 0
    recommendations = []
    
    personal_data_to_check = extract_personal_data(name, dob)
    password_lower = password.lower()
    
    found_personal_data = []
    for data in personal_data_to_check:
        if data in password_lower:
            found_personal_data.append(data)
            
    if found_personal_data:
        recommendations.append(f"Уникайте особистих даних. Знайдено: {', '.join(found_personal_data)}")
        score -= 5
    
    if len(password) >= 12:
        score += 3
    elif len(password) >= 8:
        score += 1
    else:
        recommendations.append("Пароль занадто короткий. Рекомендована довжина - 12+ символів.")

    special_chars = string.punctuation
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in special_chars for c in password)

    if has_lower:
        score += 1
    
    if has_upper:
        score += 2
    else:
        recommendations.append("Додайте великі літери.")
        
    if has_digit:
        score += 2
    else:
        recommendations.append("Додайте цифри.")
        
    if has_special:
        score += 2
    else:
        recommendations.append("Додайте спеціальні символи (наприклад, !@#$).")
        
    final_score = max(1, min(10, score))
    
    if not recommendations and final_score > 8:
        recommendations.append("Пароль виглядає надійним.")
    
    return final_score, recommendations

password_input = "ivan1995"
name_input = "Іван"
dob_input = "15.03.1995"

print(f"Аналіз для пароля: {password_input}")
print(f"Ім'я: {name_input}")
print(f"Дата народження: {dob_input}")
print("---")

score, recs = analyze_password(password_input, name_input, dob_input)

print(f"Оцінка: {score}/10")
print("Рекомендації:")
for r in recs:
    print(f"- {r}")

print("\n" + "="*20 + "\n")

password_input_2 = "My$tr0ngP@ssw0rd!"
name_input_2 = "Анна"
dob_input_2 = "10.10.2000"

print(f"Аналіз для пароля: {password_input_2}")
print(f"Ім'я: {name_input_2}")
print(f"Дата народження: {dob_input_2}")
print("---")

score_2, recs_2 = analyze_password(password_input_2, name_input_2, dob_input_2)

print(f"Оцінка: {score_2}/10")
print("Рекомендації:")
for r in recs_2:
    print(f"- {r}")