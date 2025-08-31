import requests
import random

my_key = '51d448b3'


parm = {
    's': None, #Movie genre
    't': None,  # Movie title to search for
    'type': None,  # Type of result to return.
    'y': None  # Year of release.
}

GENRES = [
    'comedy', 'drama', 'thriller', 'horror',
    'fiction', 'fantasy','romance',
    'action movie', 'adventure', 'western', 'musical','documentary']


def filter_film():
    def decorator_filtr_film_serial(func):
         typ = {
           'movie': 'filmu',
           'series': 'serialu'
           }
         def wrapper(type):
              if type not in typ:
                  raise ValueError("Nieprawidłowy typ")

              print(f'Zaczynamy podbór {typ[type]}')
              while True:
                  try:

                    s_geners = input(f'Jaki gatunek {typ[type]} chcesz wybrać?')
                    if not s_geners:
                        raise ValueError("Gatunek nie może być pusty")

                    if s_geners in GENRES:
                        parm['s'] = s_geners
                        break
                    else:
                        random_element = random.choice(GENRES)
                        ok_or_no = input(f'Nie checesz zobaczyć coś z gatunku {random_element}?')
                        if ok_or_no == 'ok':
                            parm['s'] = random_element
                            break

                  except ValueError as ve:
                      print(f"Błąd: {ve}")
                      continue

              year = input(f'Dobrze, teraz musisz wpisać rok wyproduktowania {typ[type]}')
              parm['y'] = year
              parm['type'] = type

         return wrapper

    @decorator_filtr_film_serial
    def series(type):
        pass

    @decorator_filtr_film_serial
    def movie(type):
        pass


    while True:
       type = input('Jaki gatunek filmu chcesz wybrać? [series/movie]')
       if type == 'series':
           series(type)
           break

       elif type == 'movie':
           movie(type)
           break

       else:
           print('Musisz wpisać "series" lub "movie"')


def pretty_print_movies(data):
    try:
        if data.get('Response') == 'False':
            print("Brak wyników wyszukiwania")
            return

        print(f"\nZnaleziono {data['totalResults']} wyników:")
        print("-" * 50)

        for i, movie in enumerate(data['Search'], 1):
            poster = "Brak plakatu" if movie['Poster'] == 'N/A' else "Dostępny plakat"
            print(f"{i}. {movie['Title']} ({movie['Year']})")
            print(f"   Typ: {movie['Type']}")
            print(f"   IMDb ID: {movie['imdbID']}")
            print(f"   Poster: {poster}")
            print("-" * 50)

    except ValueError as ve:
        print(f"Błąd danych: {ve}")
    except Exception as e:
        print(f"Błąd podczas wyświetlania wyników: {e}")


def show_kino_name(parm):

    if not any(parm.values()):
        raise ValueError("Brak parametrów wyszukiwania")

    url = f'http://www.omdbapi.com/?apikey={my_key}'

    if parm['s']:
        url += f'&s={parm["s"]}'
    if parm['t']:
        url += f'&t={parm["t"]}'
    if parm['type']:
        url += f'&type={parm["type"]}'
    if parm['y']:
        url += f'&y={parm["y"]}'

    try:
       r = requests.get(url, timeout=10)
       result = r.json()
       pretty_print_movies(result)

    except requests.exceptions.Timeout:
            raise TimeoutError("Przekroczono czas oczekiwania na odpowiedź serwera")

def main():
    while True:
        try:
            res = input('Potrzebujesz pomocy w wybraniu filmu lub serialu?')
            if res.capitalize() == 'Nie':
                movie = input('Informacje o jakiem filmu lub serialu chcesz otrzymać?')
                parm['t'] = movie
                show_kino_name(parm)
                break
            elif res.capitalize() == 'Tak':
                filter_film()
                show_kino_name(parm)
                break
            elif res.capitalize() == 'Zakończ':
                print('Program zakończony!')
                break
            else:
                print('Musisz wpisać "Tak", "Nie" lub "Zakończ"')

        except KeyboardInterrupt:
            print("\nPrzerwano przez użytkownika. Zamykanie programu...")
            break
if __name__ == '__main__':
    main()
