import sys
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# проверяем задали ли название сайта из консоли
def сhecking_the_string_parameters():
    if len(sys.argv) < 2:
        site_name = input_name_from_console()
        return site_name
    elif len(sys.argv) >= 2:
        site_name = sys.argv[1]
        return site_name


# вводим адрес сайта вручную если не задали  из консоли
def input_name_from_console():
    site_name = input("Введите адрес сайта ")
    print('Введена вот такая ссылка: ', site_name)
    return site_name


# парсим страничку
def crawl_pages_at_url(page_url, site_url):
    broken_links = []
    crawl_pages = []
    if site_url not in page_url:  # если ссылка внешняя
        return
    r = requests.get(page_url)  # получаем обратно обьект типа requests
    soup = BeautifulSoup(r.text, 'html.parser')  # скармливаем обьект типа реквест и указываем .text что бы получить из него только текст, и указываем в качестве синтаксического анализатора (парсера) html.parser
    for link in soup.find_all('a'):  # магия указанная в типичном способе выдирания ссылок в бьютифол супе
        link_on_page = check_suitability_of_link(link, page_url)
        print(link_on_page)
        if not link_on_page:
            continue
        if is_link_broken(link_on_page):
            broken_links.append(link_on_page)
        if is_link_html_check(link_on_page):
            crawl_pages.append(link_on_page)
    return crawl_pages, broken_links


# првоеряем что нам дают верный ответ
def is_link_broken(url):
    req = requests.head(url)
    return req.status_code not in status_code


# проверяем что это шттп что бы не гетить все подряд
def is_link_html_check(url):
    req = requests.head(url)
    return req.headers['Content-Type'] == 'text/html'


# проверяем на относительные ссылки и прочие
def check_suitability_of_link(link, page_url):
    link_name = str(link.get('href'))
    if link_name == "": #or link_name.startswith("#"):  # избавляемся от меню и прочего начниаюшегося с #
        return False
    absolute_link = urljoin(page_url, link_name)
    link_pars = urlparse(absolute_link)
    absolute_link = absolute_link.split("#")
    absolute_link = str(absolute_link[0])
    if link_pars.scheme == "tel" or link_pars.scheme == "mailto": #отсеиваем телефоны и емейлы
        return False
    else:
        return absolute_link


if __name__ == '__main__':
    visited_links = []
    external_links = []
    page_list = []
    broken_links = []
    status_code = [200, 301, 302]
    if len(sys.argv) < 2:
        site = input_name_from_console()
    else:
        site = sys.argv[1]
    crawl_pages_started, broken = crawl_pages_at_url(site, site)
    broken_links += broken
    visited_links.append(site)  # добавляем к списку посещенных страниц что бы не ходить дважды на одну страницу
    page_list.extend(crawl_pages_started)
    for page in page_list:
        if page in visited_links:
            continue
        elif site not in page:
            continue
        elif page not in visited_links:
            crawl_pages_in_a_cycle = []
            crawl_pages_in_a_cycle, page_broken_links = crawl_pages_at_url(page, site)
            broken_links += page_broken_links
            if crawl_pages_in_a_cycle is None:
                external_links.append(page)  # добавляем к списку внешних ссылок
            visited_links.append(page)
            page_list.extend(crawl_pages_in_a_cycle)
            print(page)
    print("Мы проверили ваш сайт: ", site)
    print ("Вот битые ссылки", broken_links)