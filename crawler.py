import requests
from bs4 import BeautifulSoup


def take_name():
    site_name = input("Введите адрес сайта ")
    print(site_name)
    return site_name


def crawler(aaa):
    page_name = aaa
    visited_links.append(page_name) # добавляем к списку посещенных страниц что бы не ходить дважды на одну страницу
    r = requests.get(page_name)  # получаем обратно обьект типа requests
    soup = BeautifulSoup(r.text, 'html.parser')  # скармливаем обьект типа реквест и указываем .text что бы получить из него только текст, и указываем в качестве синтаксического анализатора (парсера) html.parser
    for link in soup.find_all('a'):  # магия указанная в типичном способе выдирания ссылок в бьютифол супе
        link_name = str(link.get('href'))
        if site not in link_name: # если ссылка внешняя
            external_links.append(link.get('href'))  #добавляем к списку внешних ссылок
        elif site in link_name: # если ссылка внутреняя
            if link_name not in page_list: #проверяем что мы её ещё не добавляли
                page_list.append(link.get('href'))  # добавляем к списку всех ссылок

if __name__ == '__main__':
    visited_links = []
    external_links = []
    page_list = []
    site = take_name()
    a = crawler(site)
    for page in page_list:
        if page in visited_links:
            pass
        elif page not in visited_links:
            print(page)
            crawler(page)

    print(external_links)





#Сделай скрипт, который будет просить ввести имя сайта и ходить по всем ссылкам внутри него,
#в реалтайме выдавая в консоль ссылку на посещённую страницу.
#Список ссылок на внешние ресурсы выдавать в самом конце.
#Убедиться, что одну и ту же страницу не посещаешь дважды.
