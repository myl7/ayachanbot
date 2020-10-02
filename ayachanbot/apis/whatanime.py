from base64 import b64encode

import requests

from .log import log_error, log_success


def search_whatanime(file):
    file.seek(0, 2)
    size = file.tell() / 3 * 4
    file.seek(0)
    if size > 10 * 1024 * 1024:
        log_error('whatanime filesize error', 'too large')
        return

    resp = requests.post('https://trace.moe/api/search', json={
        'image': b64encode(file.read()).decode()
    })

    if resp.status_code != 200:
        log_error('whatanime request failed', resp)
        return

    results = resp.json()
    log_success('whatanime', results)
    return results
