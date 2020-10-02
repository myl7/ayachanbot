import logging
import json
from typing import Union

import requests


def log_error(title, content):
    content = process_content(content)
    logging.error(f'{title}:{content}')


def log_success(title, content):
    content = process_content(content)
    logging.info(f'{title}:{content}')


def process_content(content: Union[str, bytes, dict, requests.Response]):
    if isinstance(content, bytes):
        content = content.decode()
    elif isinstance(content, dict):
        content = json.dumps(content, ensure_ascii=False)
    elif isinstance(content, requests.Response):
        content = content.content.decode()
    else:
        content = str(content)

    content = content.strip()
    if content.startswith('<!DOCTYPE'):
        # content is HTML, remove duplicated spaces.
        content = ' '.join(content.split())

    return content
