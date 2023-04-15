import requests
url = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}
payload = {'from_date': <временная метка в формате Unix time>}.
# Делаем GET-запрос к эндпоинту url с заголовком headers и параметрами params
homework_statuses = requests.get(url, headers=headers, params=payload)
# Печатаем ответ API в формате JSON
print(homework_statuses.text)
# А можно ответ в формате JSON привести к типам данных Python и напечатать и его
# print(homework_statuses.json())