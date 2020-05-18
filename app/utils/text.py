from multiprocessing import Pool
from multiprocessing import cpu_count
from functools import lru_cache
import re

import pymorphy2
from nltk.corpus import stopwords

stop_words = stopwords.words('russian')
morph = pymorphy2.MorphAnalyzer()


def normalize(year):
    """
    Нормализует файл отчета за определенный год и записывает его по пути
        app/static/data/norm/CBR_report<год>_norm.txt

    :param year: Год отчета
    :type year: str/int

    :return: None
    """

    fname = f'app/static/data/txt/CBR_report{year}.txt'
    with open(fname, 'r', encoding='utf8') as f:
        with Pool(processes=cpu_count()) as pool:
            normalized_text = '\n'.join(pool.map(normalize_text, f.readlines()))
    fname = f'app/static/data/norm/CBR_report{year}_norm.txt'
    with open(fname, 'w', encoding='utf8') as f:
        f.write(normalized_text)


def normalize_text(text):
    """
    Нормализовать все слова в заданном тексте

    :param text: Текст для нормализации
    :type text: str

    :return: Нормализованный текст
    :rtype: str
    """

    result = [normalize_word(word) for word in re.findall(r'[a-zа-яё]+',
                                                          text.lower())
              if word not in stop_words]
    return ' '.join(result)


@lru_cache(maxsize=10000000)
def normalize_word(word):
    """
    Получить нормальную форму одного слова на русском языке
    Пример:
        красивая -> красивый
        детей -> ребенок

    :param word: Слово
    :type word: str

    :return: Нормальная форма слова
    :rtype: str
    """

    return morph.normal_forms(word)[0]
