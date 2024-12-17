from bs4 import BeautifulSoup
import re
import requests
from config import *

html = """
<div class="page-header-image">
    <span class="userinitials size-100" title="Андрей Бабкин" aria-label="Андрей Бабкин" role="img">АБ</span>
</div>
<div class="page-header-headings">
    <h2 class="h2 mb-0">Андрей Бабкин</h2>
</div>
</div><div class="profile_tree"><section class="node_category card d-inline-block w-100 mb-3"><div class="card-body"><h3 class="lead">Подробная информация о пользователе</h3><ul><li class="contentnode"><dl><dt>Адрес электронной почты</dt><dd><a href="ma&#105;&#108;to:%62%61a%32%38%30%36%30%39@%67%6d%61%69%6c%2e%63%6f%6d">&#98;&#97;&#97;&#50;&#56;&#48;&#54;&#48;&#57;@g&#109;&#97;&#105;l&#46;&#99;&#111;m</a></dd></dl></li><li class="contentnode"><dl><dt>Страна</dt><dd>Россия</dd></dl></li><li class="contentnode"><dl><dt>Город</dt><dd>Москва</dd></dl></li><li class="contentnode"><dl><dt>Часовой пояс</dt><dd>Europe/Moscow</dd></dl></li></ul></div></section><section class="node_category card d-inline-block w-100 mb-3"><div class="card-body"><h3 class="lead">Информация о курсах</h3><ul><li class="contentnode"><dl><dt>Участник курсов</dt><dd><ul><li><a href="https://sdo24.1580.ru/user/view.php?id=1881&amp;course=20">Информатика. ОГЭ (9: А, В, Д, Е, Ж, З, И, К, Л, М, Н, П, Р, С, Т, У, Ф)</a></li><li><a href="https://sdo24.1580.ru/user/view.php?id=1881&amp;course=23">Информатика (9: Ж, И)</a></li><li><a href="https://sdo24.1580.ru/user/view.php?id=1881&amp;course=57">Проектная мастерская, индивидуальный проект (8-10 классы)</a></li><li>Информатика. Семестровые работы и зачеты</li></ul></dd></dl></li><li class="contentnode"><dl><dt>Роли</dt><dd><a href="https://sdo24.1580.ru/user/index.php?contextid=192&amp;roleid=5">Ученик</a></dd></dl></li><li class="contentnode"><dl><dt>Группа</dt><dd> <a href="https://sdo24.1580.ru/user/index.php?id=58&amp;group=2072">09И2</a></dd></dl></li></ul></div></section><section class="node_category card d-inline-block w-100 mb-3"><div class="card-body"><h3 class="lead">Разное</h3><ul><li><span><a href="https://sdo24.1580.ru/user/profile.php?id=1881">Профиль полностью</a></span></li><li><span><a href="https://sdo24.1580.ru/mod/forum/user.php?id=1881&amp;course=58">Сообщения форумов</a></span></li><li><span><a href="https://sdo24.1580.ru/mod/forum/user.php?id=1881&amp;mode=discussions&amp;course=58">Темы форумов</a></span></li></ul></div></section><section class="node_category card d-inline-block w-100 mb-3"><div class="card-body"><h3 class="lead">Входы в систему</h3><ul><li class="contentnode"><dl><dt>Последний доступ к курсу</dt><dd>воскресенье, 8 декабря 2024, 14:28&nbsp; (8 дн. 23 час.)</dd></dl></li></ul></div></section></div></div></div>
"""

def extract_info(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Извлечение ФИО
    full_name = soup.find('h2', class_='h2 mb-0').get_text(strip=True)

    # Извлечение email
    email_link = soup.find('a', href=re.compile(r'mailto:'))
    if email_link:
        email = email_link.get_text(strip=True)
    else:
        email = None

    return full_name, email

# Вызов функции и вывод результата
fio, email = extract_info(html)
print(f"ФИО: {fio}")
print(f"Email: {email}")



def fetch_html(course_id: int) -> str:
    url = f"https://sdo24.1580.ru/user/view.php?id=1881&course={course_id}"
    headers = {
        "Cookie": "MoodleSession=isv7am1rkctrf89t8ktu6u18qt; MOODLEID1_=sodium%3AbE0wkD88jzvUPgzNS5f8M0cx%2F4%2Blqal9i9CD3GoZngVbIyx8GrrwaW7%2FrphAFN%2FOdrY%3D"
    }
    
    response = requests.get(url, headers=headers)
    
    # Проверяем, успешен ли запрос
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

# Пример использования функции
if __name__ == "__main__":
    course_number = 56 # Замените на нужное число
    try:
        html_content = fetch_html(course_number)
        print(html_content)  # Выводим HTML-контент
    except Exception as e:
        print(e)

