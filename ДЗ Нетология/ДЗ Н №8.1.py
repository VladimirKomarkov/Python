import requests

response = requests.get("https://akabab.github.io/superhero-api/api/all.json")

names = ['Hulk', 'Captain America', 'Thanos']
intelligence = []
for i in response.json():
    for j in i.values():
        if j in names:
            intelligence.append(i["powerstats"]['intelligence'])

name_int = dict(zip(names, intelligence))

names_sorted = sorted(name_int.items(), key=lambda x: x[1], reverse=True)
print(f'Самый умный супергерой - {names_sorted[0][0]}, его интеллект составляет '
      f'{names_sorted[0][1]} баллов!')















