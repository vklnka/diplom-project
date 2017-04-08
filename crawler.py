import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    site_name = input("Введите адрес сайта ")
    r = requests.get(site_name) #получаем обратно обьект типа requests
    soup = BeautifulSoup(r.text, 'html.parser') #скармливаем обьект типа реквест и указываем .text что бы получить из него только текст, и указываем в качестве синтаксического анализатора (парсера) html.parser
    for link in soup.find_all('a'): #магия указанная в типичном способе выдирания ссылок в бьютифол супе
        print(link.get('href'))