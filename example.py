import requests
from bs4 import BeautifulSoup
import os
import datetime
import re

def get_cve_list():
    # Функция для получения списка новых CVE за сегодняшний день
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    url = 'https://cve.mitre.org/data/downloads/allitems.csv'
    response = requests.get(url)
    cve_list = response.text.splitlines()[1:]  # пропускаем заголовок
    today_cves = [cve_entry for cve_entry in cve_list if cve_entry.split(',')[2] == today]  # фильтруем по дате
    return today_cves

def search_github(cve):
    # Функция для поиска упоминаний CVE на GitHub
    url = f'https://github.com/search?q={cve}+language%3A{cve}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('a', class_='v-align-middle')
    github_urls = [result['href'] for result in results if 'github.com' in result['href']]
    return github_urls

def download_code(url, cve):
    # Функция для загрузки кода из GitHub
    response = requests.get(url)
    filename = f"{cve}_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    with open(filename, 'w') as f:
        f.write(response.text)
    print(f"Код для CVE {cve} был сохранен в файле: {filename}")

def main():
    cve_list = get_cve_list()
    if cve_list:
        print(f"Найдены новые CVE за сегодняшний день:")
        for cve_entry in cve_list:
            cve = cve_entry.split(',')[0]  # Получаем только номер CVE
            github_urls = search_github(cve)
            if github_urls:
                print(f"Найдены упоминания для CVE {cve}:")
                for url in github_urls:
                    print(url)
                    download_code(url, cve)
            else:
                print(f"Для CVE {cve} не найдены упоминания на GitHub.")
    else:
        print("На сегодня новых CVE не найдено.")

if __name__ == "__main__":
    main()
