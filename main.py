import os
import xlrd
from htpasswd import HtpasswdFile


def main():
    xlslist = xlrd.open_workbook('list.xls')
    sheet = xlslist.sheet_by_index(0)

    basedir = 'Учителя'

    if not os.path.exists(basedir):
        os.mkdir(basedir)

    for row in range(sheet.nrows):
        for col in range(sheet.ncols):
            cell_value = sheet.cell_value(row, col)
            familia, name, otchestvo = cell_value.split()
            personal_dir = os.path.join(basedir, f'{familia} {name} {otchestvo}')
            translit_fio = get_translit_fio(familia, name, otchestvo)
            user_password = get_user_password(translit_fio)
            if not os.path.exists(personal_dir):
                os.mkdir(personal_dir)

                file_path = os.path.join(personal_dir, f"{translit_fio['familia']}.bat")

                bat_script = f"""@echo off
setlocal

set "WebDAV_Address=91.197.207.176"
set "Username={translit_fio['familia']}_{translit_fio['name'][0]}{translit_fio['otchestvo'][0]}"
set "Password={user_password}"
set "DriveLetter=S"

net use %DriveLetter% "http://%Username%:%Password%@%WebDAV_Address%" /PERSISTENT:YES

if errorlevel 1 (
    echo Подключение не удалось.
    pause
    exit /b 1
) else (
    echo Подключение к S: успешно установлено.
    pause
)

exit /b 0"""
                with open(file_path, 'w', encoding='cp866') as file:
                    file.write(bat_script)
                file.close()


def translit(text):
    translate_dict = {
        'а': 'a',
        'б': 'b',
        'в': 'v',
        'г': 'g',
        'д': 'd',
        'е': 'e',
        'ё': 'e',
        'ж': 'zh',
        'з': 'z',
        'и': 'i',
        'й': 'y',
        'к': 'k',
        'л': 'l',
        'м': 'm',
        'н': 'n',
        'о': 'o',
        'п': 'p',
        'р': 'r',
        'с': 's',
        'т': 't',
        'у': 'u',
        'ф': 'f',
        'х': 'h',
        'ц': 'c',
        'ч': 'ch',
        'ш': 'sh',
        'щ': 'shch',
        'ъ': '',
        'ь': '',
        'ю': 'yu',
        'я': 'ya',
    }

    text = text.lower()
    trans_table = text.maketrans(translate_dict)
    result = text.translate(trans_table)
    return result


def get_translit_fio(familia, name, otchestvo):
    trans_familia = translit(familia)
    trans_name = translit(name)
    trans_otchestvo = translit(otchestvo)
    return {
        'familia': trans_familia,
        'name': trans_name,
        'otchestvo': trans_otchestvo
    }


def get_user_password(string_dict):
    familia = string_dict['familia']
    name = string_dict['name']
    otchestvo = string_dict['otchestvo']

    # Получаем количество символов в каждой строке
    len_familia = len(familia)
    len_name = len(name)
    len_otchestvo = len(otchestvo)

    # Получаем первую и предпоследнюю букву из каждой строки
    first_chars = [familia[0], name[0], otchestvo[0]]
    penultimate_chars = [familia[-2], name[-2], otchestvo[-2]]

    # Преобразовываем буквы в соответствии с правилами
    result_chars = [
        first_chars[0].lower(),
        first_chars[1].lower(),
        first_chars[2].upper(),
        penultimate_chars[0].lower(),
        penultimate_chars[1].lower(),
        penultimate_chars[2].upper()
    ]

    # Собираем строку
    result_string = ''.join(result_chars)

    # Вычисляем общее количество букв в трех строках и делим на 4 с остатком
    total_length = len_familia + len_name + len_otchestvo
    remainder = total_length // 4

    # Добавляем к строке результат деления с остатком
    result_string = str(total_length % 6) + result_string + str(remainder)

    return result_string


def generate_htpasswd_file(username, password, output_file):
    htpasswd = HtpasswdFile(output_file)
    htpasswd.update({username: password})
    htpasswd.close()


if __name__ == '__main__':
    main()
