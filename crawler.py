import sys
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# проверяем задали ли название сайта из консоли
def сhecking_the_string_parameters():
    if len(sys.argv) < 2:
        site = input_name_from_console()
        return site
    elif len(sys.argv) >= 2:
        site = sys.argv[1]
        return site


# вводим адрес сайта вручную если не задали  из консоли
def input_name_from_console():
    site_name = input("Введите адрес сайта ")
    print('Введена вот такая ссылка: ', site_name)
    return site_name


# парсим страничку
def crawl_pages_at_url(page_url):
    crawl_pages = []
    visited_links.append(page_url)  # добавляем к списку посещенных страниц что бы не ходить дважды на одну страницу
    if site not in page_url:  # если ссылка внешняя
        external_links.append(page_url)  # добавляем к списку внешних ссылок
        return False
    r = requests.get(page_url)  # получаем обратно обьект типа requests
    soup = BeautifulSoup(r.text, 'html.parser')  # скармливаем обьект типа реквест и указываем .text что бы получить из него только текст, и указываем в качестве синтаксического анализатора (парсера) html.parser
    for link in soup.find_all('a'):  # магия указанная в типичном способе выдирания ссылок в бьютифол супе
        link_on_page = check_suitability_of_link(link, page_url)
        if link_on_page:
            crawl_pages.append(link_on_page)
    page_list.extend(crawl_pages)


# проверяем на относительные ссылки и прочие
def check_suitability_of_link(link, page_url):
    link_name = str(link.get('href'))
    if link_name == "":
        return False
    elif link_name[0] == "#": #избавляемся от меню и прочего начниаюшегося с #
        return False
    absolute_link = urljoin(page_url, link_name)
    link_pars = urlparse(absolute_link)
    if link_pars.scheme == "tel" or link_pars.scheme == "mailto": #отсеиваем телефоны и емейлы
        return False
    else:
        return absolute_link


if __name__ == '__main__':
    visited_links = []
    external_links = []
    page_list = []

    if len(sys.argv) < 2:
        site = input_name_from_console()
    elif len(sys.argv) >= 2:
        print(sys.argv[1])

    crawl_pages_at_url(site)
    for page in page_list:
        if page in visited_links:
            pass
        elif site not in page:
            pass
        elif page not in visited_links:
             crawl_pages_at_url(page)
             print(page)
    print("Мы проверили ваш сайт: ", site)