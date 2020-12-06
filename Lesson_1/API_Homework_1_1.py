import requests
import json
from pprint import pprint

# Выдвет мои репозитории, которые я создавал для обучения. Других просто нет, т.к до начала обучения не работал ни с гитом ни с программированием в целом
# В комментах строчки с помощью которых пытался разобраться и найти то что мне было необходимо
username = 'ArtisticPug'

main_link = f'https://api.github.com/users/{username}/repos'

response = requests.get(main_link)

status_code = response.status_code

if status_code == 200: # status_code.ok не работает, а почему не работает я не понял
    j_data = response.json()
    repos_names_list = []
    # print(type(j_data))
    for el in j_data:
        # print((list(el.items())[2][0]), (list(el.items())[2][1]))
        repos_names_list.append({(list(el.items())[2][0]): (list(el.items())[2][1])})
        print(repos_names_list)
    for el in repos_names_list:
        print(type(el))
    # pprint(j_data[0].keys())
    # pprint(j_data[0].get('name'))
    # pprint(j_data[0].get('full_name'))
    with open("my_git_repos.json", "w") as write_repos:
        json.dump(repos_names_list, write_repos)
else:
    print('Ошибка')
