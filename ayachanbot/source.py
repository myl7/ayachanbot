import json

import requests
import yaml


def search_saucenao(file):
    resp = requests.post('https://saucenao.com/search.php', {
        'frame': 1,
        'hide': 0,
        'database': 999,
        'output_type': 2
    }, files={'file': file})
    result = json.loads(resp.content.decode())['results'][0]
    text = f"{yaml.dump(result['header'], allow_unicode=True)}\n\
        {yaml.dump(result['data'], indent=2, allow_unicode=True)}"
    return text


def search_ascii2d(file):
    return NotImplementedError()


def search_nhentai(file):
    return NotImplementedError()


def search_whatanime(file):
    return NotImplementedError()
