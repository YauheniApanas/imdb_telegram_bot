from config import config
from typing import Dict, List
import requests
import json


token = config.api_token.get_secret_value()


def search(title: str) -> Dict:
    url = f'https://imdb-api.com/ru/API/Search/{token}/{title}'
    print(url)
    res = json.loads(requests.get(url=url).text)
    print(res)
    dict_res = dict()
    for _ in range(3):
        dict_res[res['results'][_]['title']] = res['results'][_]['id']
    return dict_res


def get_info(title_id: str) -> Dict:
    url = f'https://imdb-api.com/ru/API/Title/{token}/{title_id}'
    print(url)
    res = json.loads(requests.get(url=url).text)
    dict_res = dict()
    dict_res['title'] = res['fullTitle']
    dict_res['type'] = res['type']
    dict_res['image'] = res['image']
    dict_res['plot'] = res['plotLocal']
    dict_res['directors'] = res['directors']
    dict_res['date'] = res['releaseDate']
    dict_res['genre'] = res['genres']
    dict_res['rating'] = res['imDbRating']
    dict_res['countries'] = res['countries']
    dict_res['similars'] = res['similars']
    dict_res['id'] = res['id']

    def get_yt_trailer():
        url = f'https://imdb-api.com/ru/API/YouTubeTrailer/{token}/{title_id}'
        return json.loads(requests.get(url=url).text)

    yt_url = get_yt_trailer()['videoUrl']
    dict_res['trailer'] = yt_url
    return dict_res


def genres_search(genre: str) -> List:
    url = f'https://imdb-api.com/ru/API/AdvancedSearch/{token}?genres={genre}'
    res_dict = json.loads(requests.get(url=url).text)
    return res_dict['results']


def rating_search(rating: str) -> List:
    rating_edited = f'{rating.split()[0]},{rating.split()[1]}'
    url = f'https://imdb-api.com/ru/API/AdvancedSearch/{token}?user_rating={rating_edited}'
    res_dict = json.loads(requests.get(url=url).text)
    return res_dict['results']


def get_series() -> List:
    url = f'https://imdb-api.com/ru/API/Top250TVs/{token}'
    return json.loads(requests.get(url=url).text)['items']


def get_movies() -> List:
    url = f'https://imdb-api.com/ru/API/Top250Movies/{token}'
    return json.loads(requests.get(url=url).text)['items']
