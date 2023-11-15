import re
from pprint import pprint
import csv

def format_phone(phone):
    # Приводим телефон к формату +7(999)999-99-99
    phone = re.sub(r'(\+7|8)?[\s\(\)\-]*([4895][0-9]{2})[\s\(\)\-]*([0-9]{3})[\s\(\)\-]*([0-9]{2})[\s\(\)\-]*([0-9]{2})[\s\(\)\-]*(доб\.[0-9]+)?', r'+7(\2)\3-\4-\5 \6', phone)
    return phone

def merge_duplicates(contacts_list):
    # Создаем словарь для хранения уникальных записей по номеру телефона
    unique_contacts = {}

    for contact in contacts_list:
        phone = contact[5]  # Предполагаем, что телефон уникальный
        if phone in unique_contacts:
            # Объединяем записи
            unique_contacts[phone].update(contact)
        else:
            unique_contacts[phone] = set(contact)

    # Преобразуем словарь обратно в список
    merged_contacts = [list(contact) for contact in unique_contacts.values()]

    return merged_contacts

def process_contacts(contacts_list):
    for contact in contacts_list:
        # Разбиваем поле "ФИО" на фамилию, имя и отчество
        full_name = re.split(r'\s+', contact[0])
        if len(full_name) == 1:
            # Если только фамилия, оставляем как есть
            contact[0], contact[1], contact[2] = full_name[0], '', ''
        elif len(full_name) == 2:
            # Если фамилия и имя
            contact[0], contact[1], contact[2] = full_name[0], full_name[1], ''
        elif len(full_name) >= 3:
            # Если фамилия, имя и отчество
            contact[0], contact[1], contact[2] = full_name[0], full_name[1], ' '.join(full_name[2:])

        # Приводим телефон к нужному формату
        contact[5] = format_phone(contact[5])

    # Объединяем дубликаты
    contacts_list = merge_duplicates(contacts_list)

    return contacts_list

# Читаем адресную книгу в формате CSV в список contacts_list
with open("C:\\Python\\ДЗ Нетология\\Regular Expressions\\phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Обрабатываем данные
contacts_list = process_contacts(contacts_list)

# Сохраняем получившиеся данные в новый файл в формате CSV
with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)

# Выводим результат для проверки
pprint(contacts_list)
