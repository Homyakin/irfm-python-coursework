import os
import re
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

base_url = "https://cbr.ru/about_br/publ/god/"
cbr_home = "https://cbr.ru"


def get_links():
    """
    Возвращает ссылки, по которым доступны годовые отчеты на сайте ЦБ РФ

    :return: Словарь вида "год": "сслыка"
    :rtype: dict of string:string
    """

    response = requests.get(base_url)
    content = response.content.decode()
    soup = BeautifulSoup(content, features="lxml")
    tags = soup.find_all('a', {'class': 'versions_item'})
    links = {}
    for tag in tags:
        name = re.search(r'\d{4}', tag.text)[0]
        link = urljoin(cbr_home, tag.attrs['href'])
        links[name] = link

    return links


def download_pdf(link, year):
    """
    Загружает с сайта ЦБ отчет по переданной ссылке

    :param link: URL документа
    :type link: str
    :param year: Год отчета
    :type year: str/int

    :return: Имя сохраненного документа
    :rtype: str
    """

    response = requests.get(link, stream=True)
    fname = f"app/static/data/pdf/CBR_report{year}.pdf"
    if os.path.exists(fname):
        return fname
    with open(fname, "wb") as f:
        f.write(response.content)
    return fname
