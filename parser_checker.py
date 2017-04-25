import requests
from bs4 import BeautifulSoup


def get_links(html_text, protocol , site_name):  # Функция вытаскивает ссылки
    broken_links = []
    visited_links = {}  #счетчик посещенных страниц
    soup = BeautifulSoup(html_text, "html.parser")
    external_links_cnt = 0  # Счетчик внешних ссылок
    internal_links_cnt = 0  # Счетчик внутренних ссылок
    for link in soup.find_all("a"):
        href = link.get("href")
        if href.startswith('//'):  # если ссылка начинается с //
            href = "{}:{}".format(protocol, href)  # добавим протокол к этой ссылки,чтобы ссылка стала верной
        if site_name in href:
            internal_links_cnt += 1  #Проверка внешних ссылок
        else:
            external_links_cnt += 1  #Проверка внутренних ссылок
        visited_links[href] = visited_links.get(href, 0) + 1  #если ссылки не было,значение будет единица,если была то прибавляем +1
        link_is_broken = check_broken_link(href)  # Вызов функции проверки,битая ли ссылка
        if link_is_broken:  # Если ссылка битая
            broken_links.append(href)  # Добавляем в список битых ссылок
    return broken_links, visited_links, internal_links_cnt, external_links_cnt


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
    broken_links, visited_links, internal_links_cnt, external_links_cnt = get_links(r.text, protocol, site_name)
    print("Кол-во внешних ссылок: {}, кол-во внутренних ссылок: {}, общее коли-во ссылок: {}".format(external_links_cnt, internal_links_cnt, external_links_cnt+internal_links_cnt))