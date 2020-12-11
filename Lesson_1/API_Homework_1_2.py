import requests
import json
from pprint import pprint

# Выдает случайное пиво и его характеристики

key = '543bc559d6a094b4e981a953469110c4'

main_link = f'https://sandbox-api.brewerydb.com/v2//beer/random?key={key}'

response = requests.get(main_link)
status_code = response.status_code

if status_code == 200: # status_code.ok не работает, а почему не работает я не понял
    j_data = response.json()
    pprint(j_data)
    with open("my_random_beer.json", "w") as write_random_beer:
        json.dump(j_data, write_random_beer)
else:
    print('Ошибка')