from pprint import pprint
import re
# читаем адресную книгу в формате CSV в список contacts_list
import csv


def read_csv():
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


def get_correct_contacts_list(contscts_list: list):
    for item in contscts_list:
        name_reqex = re.compile(r'([а-яa-z]+)*\W*([а-яa-z]+)*\W*([а-яa-z]+)*', flags=re.IGNORECASE)
        m = name_reqex.match(' '.join((item[0], item[1], item[2])))
        item[0] = m.group(1) or ''
        item[1] = m.group(2) or ''
        item[2] = m.group(3) or ''


def write_csv(contacts_list: list):
    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        # Вместо contacts_list подставьте свой список
        datawriter.writerows(contacts_list)


if __name__ == '__main__':
    contacts_list = read_csv()
    get_correct_contacts_list(contacts_list)
