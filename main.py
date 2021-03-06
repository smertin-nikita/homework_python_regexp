from copy import deepcopy
import re
# читаем адресную книгу в формате CSV в список contacts_list
import csv


def read_csv():
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


def write_csv(contacts_list: list):
    with open("phonebook.csv", "w",  encoding='utf-8', newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)


def get_fullname(lastname: str, firstname: str, surname: str):
    return ' '.join((lastname, firstname, surname))


def set_correct_names(contacts_list: list):
    temp = deepcopy(contacts_list)
    for item in temp[1:]:
        regexp = re.compile(r'([а-яa-z]+)?\W*([а-яa-z]+)?\W*([а-яa-z]+)?', flags=re.IGNORECASE)
        m = regexp.match(get_fullname(*item[:3]))
        # Если группа None то присвоить пустую строку
        item[0] = m.group(1) or ''
        item[1] = m.group(2) or ''
        item[2] = m.group(3) or ''
    return temp


def set_correct_phones(contacts_list: list):
    temp = deepcopy(contacts_list)
    for item in temp[1:]:
        regex = re.compile(r'(\+7|8)?[\s\(-]*(\d{3})[\s\)-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})[\(\s]*(доб\.)?\s*(\d+)?.*')
        item[5] = regex.sub(r"+7(\2)\3-\4-\5 \6\7", item[5]).rstrip(' ')
    return temp


def remove_duplicates(contacts_list: list, compare_index=2):
    """
    Сначала ищет соовпадения у списков по compare_index(по именам),
    затем не пустые значения записыются во второй список из совпавших,
    а первый удалется.
    """
    temp = deepcopy(contacts_list)
    for item in temp:
        i = temp.index(item)
        for ditem in temp[i+1:]:
            # По имени и фамилии если compare_index = 2
            if item[:compare_index] == ditem[:compare_index]:
                for j in range(len(ditem)-1):
                    # присваиваю второму списку значения из первого если не пустые
                    ditem[j] = ditem[j] or item[j]
                temp.remove(item)
                break
    return temp


if __name__ == '__main__':
    contacts_list = read_csv()
    correct_contacts = set_correct_phones(set_correct_names(contacts_list))
    correct_contacts = remove_duplicates(correct_contacts)
    write_csv(correct_contacts)
