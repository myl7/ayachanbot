import json

import requests

from .log import log_error, log_success


def search_saucenao(file):
    resp = requests.post('https://saucenao.com/search.php', {
        'frame': 1,
        'hide': 0,
        'database': 999,
        'output_type': 2
    }, files={'file': file})

    if resp.status_code != 200:
        log_error('saucenao request failed', resp)
        return

    content = json.loads(resp.content.decode())
    # Remove result count status in every databases: Too long and meaningless.
    content['header'].pop('index')
    log_success('saucenao', content)
    return content['results']
