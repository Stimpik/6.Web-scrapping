import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json

url = 'https://spb.hh.ru/search/vacancy?area=1&area=2&enable_snippets=true&ored_clusters=true&text=python+%2C+django%2C+flask&search_period=1'

def get_headers():
    headers = Headers(browser='firefox', os= 'win')
    return headers.generate()

response = requests.get(url, headers=get_headers()).text
soup = BeautifulSoup(response, features='lxml')


serp_item = soup.find('div', class_="vacancy-serp-content").find_all('div', class_="serp-item")

info = []

for item in serp_item:
    try:
        salary = item.find('span', class_="bloko-header-section-3").text
    except:
        salary = 'Размер не указан'
    vacancy_name = item.find('a', class_= "serp-item__title").text
    company_name = item.find('a', class_="bloko-link bloko-link_kind-tertiary").text
    city = item.find('div', attrs={'data-qa' : 'vacancy-serp__vacancy-address'}, class_= "bloko-text").text.split()[0]
    link = item.find('a')['href']
    item = {'vacancy_name' : vacancy_name,
            'company_name' : company_name,
            'city' : city,
            'link' : link,
            'salary' : salary}
    info.append(item)

with open('vacancy.json', 'w', encoding='utf-8') as file:
    json.dump(info, file, indent=5, ensure_ascii=False)


#Не нашел зарплат в USD, но предполагаю, что как-то так.


# for item in serp_item:
#     try:
#         salary = item.find('span', class_="bloko-header-section-3").text
#         if 'USD' in salary:
#         vacancy_name = item.find('a', class_="serp-item__title").text
#         company_name = item.find('a', class_="bloko-link bloko-link_kind-tertiary").text
#         city = item.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}, class_="bloko-text").text.split()[0]
#         link = item.find('a')['href']
#         item = {'vacancy_name': vacancy_name,
#                 'company_name': company_name,
#                 'city': city,
#                 'link': link,
#                 'salary': salary}
#         info.append(item)
#     except:
#         pass
