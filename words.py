import pandas as pd
import logging
import re
import os
import zipfile

# setup logging
logging.basicConfig(filename='log.txt', filemode='w', format='%(asctime)s - %(message)s',
                    level=logging.INFO)

# zip all .txt files
def zip_files():
    for_zip = zipfile.ZipFile('archive.zip', 'w')
    for file in os.listdir():
        if file.endswith('.txt'):
            for_zip.write(os.path.join(file), file, compress_type=zipfile.ZIP_DEFLATED)
    for_zip.close()
    logging.info('Упаковали файлы с результатами работы программы в архив')

# write result to file
def write_to_file(result):
    with open('result.txt', 'a', encoding="utf-8") as res_file:
        res_file.writelines(result)
        logging.info('Результат записан в файл')


# write words count to csv file
def wr_to_csv(count):
    df = pd.DataFrame.from_dict(count, orient='index').sort_values(by=[0], ascending=False)
    pd.DataFrame(df).fillna('').to_csv('table.csv')
    # print(df.head())
    logging.info('Таблица подсчета слов записана в файл table.csv')


# find longest word
def find_longest_word(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
        txt = f.read().split()  # file to list
        longest_word = max(txt, key=len)
        write_to_file('Самое длинное слово в тексте - ' + longest_word + '\n')
        logging.info('Самое длинное слово в тексте найдено')


# count words in text
def count_words(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        text = file.read().split()  # file to list
        count = {}
        for word in text:
            if word in count:
                count[word] += 1
            else:
                count[word] = 1
        logging.info('Посчитали количество вхождений каждого слова в тексте')
        wr_to_csv(count)


# find palindrome in line
def find_palindorme(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        result = []
        text_lines = [line.strip() for line in file.readlines()]
        for line in text_lines:
            line = re.sub('[,.!]', '', line)
            raw_line = line.replace(' ', '').lower()
            if raw_line == raw_line[::-1]:
                result.append(line + '\n')
                logging.info('В строке текста найден палиндром')
            else:
                pass

        write_to_file(result)


file_name = 'example.txt'

# Вывести в table.csv файл таблицу подсчета использования слов в тексте.
count_words(file_name)

# Определить, есть ли в тексте строка-палиндром, если есть, вывести ее в файл result.txt
find_palindorme(file_name)

# Найти и вывести в файл result.txt самое длинное слово в тексте
find_longest_word(file_name)

# zip files
zip_files()
