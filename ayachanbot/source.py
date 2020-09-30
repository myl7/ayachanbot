import json
import logging

import requests


def search_saucenao(file):
    resp = requests.post('https://saucenao.com/search.php', {
        'frame': 1,
        'hide': 0,
        'database': 999,
        'output_type': 2
    }, files={'file': file})
    content = resp.content.decode()

    if resp.status_code != 200:
        logging.error(f'saucenao failed:{content}')
        return

    content = json.loads(content)
    content['header'].pop('index')
    logging.info(f'saucenao:{json.dumps(content, ensure_ascii=False)}')
    return content['results']


def search_ascii2d(file):
    return NotImplementedError()


def search_nhentai(file):
    return NotImplementedError()


def search_whatanime(file):
    return NotImplementedError()
