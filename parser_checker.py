import requests
from bs4 import BeautifulSoup


def get_links(html_text, protocol):  # Функция вытаскивает ссылки
    broken_links = []
    visited_links = {}  #счетчик посещенных страниц
    soup = BeautifulSoup(html_text, "html.parser")
    for link in soup.find_all("a"):
        href = link.get("href")
        if href.startswith('//'):  # если ссылка начинается с //
            href = "{}:{}".format(protocol, href)  # добавим протокол к этой ссылки,чтобы ссылка стала верной
        visited_links[href] = visited_links.get(href, 0) + 1  #если ссылки не было,значение будет единица,если была то прибавляем +1
        link_is_broken = check_broken_link(href)  # Вызов функции проверки,битая ли ссылка
        if link_is_broken == True:  # Если ссылка битая
            broken_links.append(href)  # Добавляем в список битых ссылок
    return broken_links, visited_links


def check_broken_link(link):  # Проверяет битая ли ссылка
    try:
        req = requests.get(link)
        if req.status_code != 200:  # отсутствие успешного ответа
            return True
    except requests.exceptions.RequestException:  # ловим исключения ,которые бросает requests
        return True
    return False


if __name__ == '__main__':
    site_name = input("Введите адрес сайта ")
    print(site_name)
    r = requests.get(site_name)  # получаем обратно обьект типа requests
    protocol = site_name.split("://")[0]  # получаем протокол из введенной пользователем ссылки
    broken_links, visited_links = get_links(r.text, protocol)
