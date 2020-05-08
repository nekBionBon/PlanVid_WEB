from requests import get, post, delete

print(get('http://localhost:5000/api/film').json())

print(get('http://localhost:5000/api/film/6').json())

print(post('http://localhost:5000/api/film',
           json={'id': 4, 'name': 'второй фильм', 'genre': 'ужасы',
                 'year': '2009', 'duration': '100', 'id_author': 1, 'watched': 0,
                 'timecode': '78', 'review': 'мой второй фильм'}).json())

print(delete('http://localhost:5000/api/film/6').json())
