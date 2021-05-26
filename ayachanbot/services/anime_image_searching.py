import os
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

import requests

from ayachanbot import log, error


def search_anime_image(file):
    url = upload_image(file)
    res = {
        'saucenao': add_image_url_query('https://saucenao.com/search.php?db=999', url),
        'ascii2d': 'https://ascii2d.net/search/url/' + url,
        'tracemoe': add_image_url_query('https://trace.moe/?auto', url),
        'iqdb': add_image_url_query('https://iqdb.org', url),
        'tineye': add_image_url_query('https://www.tineye.com/search/', url),
        'yandex': add_image_url_query('https://yandex.com/images/search?rpt=imageview', url),
        'google': add_image_url_query('https://www.google.com/searchbyimage?safe=off', url, 'image_url')
    }
    log.log_service_ok('anime image searching', res)
    return res


def add_image_url_query(template_url, image_url, field=None):
    url = list(urlparse(template_url))
    qs = dict(parse_qsl(url[4]))
    qs[field if field else 'url'] = image_url
    url[4] = urlencode(qs)
    return urlunparse(url)


def upload_image(file):
    imgur_client_id = os.getenv('IMGUR_CLIENT_ID')
    res = requests.post(
        'https://api.imgur.com/3/image',
        files={'image': file},
        headers={'Authorization': f'Client-ID {imgur_client_id}'}
    )
    if res.status_code != 200:
        log.log_service_req_failed('anime image searching', res)
        raise error.AnimeImageSearchingError()
    body = res.json()
    if not body['success']:
        log.log_service_req_failed('anime image searching', res)
        raise error.AnimeImageSearchingError()
    return body['data']['link']
