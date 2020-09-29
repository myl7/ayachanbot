import json
import logging

import requests
import yaml


def search_saucenao(file):
    resp = requests.post('https://saucenao.com/search.php', {
        'frame': 1,
        'hide': 0,
        'database': 999,
        'output_type': 2
    }, files={'file': file})
    status_code = resp.status_code
    content = json.loads(resp.content.decode())
    content['header'].pop('index')

    if status_code != 200:
        log_f = logging.error
    else:
        log_f = logging.info
    log_f(f'status_code:{status_code},content:{json.dumps(content, ensure_ascii=False)}')

    result = content['results'][0]

    def dumper(section):
        return yaml.dump(result[section], allow_unicode=True)

    text = f"{dumper('header')}\n{dumper('data')}"
    return text


def search_ascii2d(file):
    return NotImplementedError()


def search_nhentai(file):
    return NotImplementedError()


def search_whatanime(file):
    return NotImplementedError()
