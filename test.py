import requests

API_KEY = '51d448b3'
url = f"http://www.omdbapi.com/?apikey={API_KEY}"

params = {
    "s": "detective",  # поиск по ключевому слову (например, жанру)
    "y": 2020,      # год
    "type": "movie"  # только фильмы
}

response = requests.get(url, params=params)
movies = response.json()["Search"]

for movie in movies:
    print(movie["Title"], "-", movie["Year"])