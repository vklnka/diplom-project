import requests
from bs4 import BeautifulSoup


def get_links(html_text, protocol):  # Функция вытаскивает ссылки
    soup = BeautifulSoup(html_text, "html.parser")
    for link in soup.find_all("a"):
        href = link.get("href")
        if href.startswith('//'):  # если ссылка начинается с //
            href = "{}:{}".format(protocol, href)  # добавим протокол к этой ссылки,чтобы ссылка стала верной
        check_link(href)


def check_link(link):  # Проверяет ссылки
    try:
        req = requests.get(link)
        if req.status_code != 200:  # отсутствие успешного ответа
            print(link)
    except requests.exceptions.RequestException:  # ловим исключения ,которые бросает requests
        print(link)


if __name__ == '__main__':
    site_name = input("Введите адрес сайта ")
    print(site_name)
    r = requests.get(site_name)  # получаем обратно обьект типа requests
    protocol = site_name.split("://")[0]  # получаем протокол из введенной пользователем ссылки
    get_links(r.text, protocol)
