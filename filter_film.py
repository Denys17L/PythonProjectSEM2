import requests
import random
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class MovieSearchParams:
    genre: Optional[str] = None
    title: Optional[str] = None
    type: Optional[str] = None
    year: Optional[str] = None


class MovieFinder:
    API_KEY = '51d448b3'
    BASE_URL = 'http://www.omdbapi.com/'

    GENRES = [
        'comedy', 'drama', 'thriller', 'horror',
        'fiction', 'fantasy', 'romance',
        'action movie', 'adventure', 'western',
        'musical', 'documentary'
    ]

    TYPE_MAPPING = {
        'movie': 'filmu',
        'series': 'serialu'
    }

    def __init__(self):
        self.params = MovieSearchParams()

    def search_by_filters(self):
        self._get_movie_type()
        self._get_genre()
        self._get_year()
        return self._make_request()

    def search_by_title(self, title: str):
        self.params.title = title
        return self._make_request()

    def _get_movie_type(self):
        while True:
            media_type = input('Co chcesz wybrać? [series/movie] ').lower()
            if media_type in self.TYPE_MAPPING:
                self.params.type = media_type
                break
            print('Musisz wpisać "series" lub "movie"')

    def _get_genre(self):
        print(f'Zaczynamy podbór {self.TYPE_MAPPING[self.params.type]}')
        while True:
            genre = input(f'Jaki gatunek {self.TYPE_MAPPING[self.params.type]} chcesz wybrać? ')
            if genre in self.GENRES:
                self.params.genre = genre
                break

            random_genre = random.choice(self.GENRES)
            choice = input(f'Może chcesz zobaczyć coś z gatunku {random_genre}? (tak/nie) ')
            if choice.lower() == 'tak':
                self.params.genre = random_genre
                break

    def _get_year(self):
        """Pobranie roku produkcji od użytkownika"""
        self.params.year = input(
            f'Podaj rok produkcji {self.TYPE_MAPPING[self.params.type]}: '
        )

    def _make_request(self) -> Dict:
        """Wykonanie zapytania do API"""
        try:
            params = {
                'apikey': self.API_KEY,
                's': self.params.genre,
                't': self.params.title,
                'type': self.params.type,
                'y': self.params.year
            }
            # Usuwamy None wartości
            params = {k: v for k, v in params.items() if v is not None}

            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()  # Sprawdza status HTTP
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'Błąd połączenia: {e}')
            return {'Response': 'False', 'Error': str(e)}
        except Exception as e:
            print(f'Niespodziewany błąd: {e}')
            return {'Response': 'False', 'Error': 'Unknown error'}


class MoviePrinter:
    @staticmethod
    def print_results(data: Dict):
        if data.get('Response') == 'False':
            error = data.get('Error', 'Nieznany błąd')
            print(f"\nBłąd wyszukiwania: {error}")
            return

        print(f"\nZnaleziono {data.get('totalResults', 0)} wyników:")
        print("-" * 60)

        for i, movie in enumerate(data.get('Search', []), 1):
            poster = "✔" if movie.get('Poster', 'N/A') != 'N/A' else "✖"
            print(f"{i}. {movie.get('Title', 'Brak tytułu')} ({movie.get('Year', '?')})")
            print(f"   Typ: {movie.get('Type', '?')}")
            print(f"   IMDb: {movie.get('imdbID', '?')}")
            print(f"   Plakat: {poster}")
            print("-" * 60)

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