import json
import logging

import requests
from bs4 import BeautifulSoup


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
    token_resp = requests.get('https://ascii2d.net/')
    token_soup = BeautifulSoup(token_resp.content.decode(), 'html.parser')
    token = token_soup.find('input', {'name': 'authenticity_token'})['value']

    color_resp = requests.post('https://ascii2d.net/search/file', {
        'utf8': '✓',
        "authenticity_token": token,
    }, files={'file': file}, headers={'Content-Type': 'multipart/form-data'})
    color_content = color_resp.content.decode()

    def compress_html(raw):
        return ' '.join(raw.split())

    if color_resp.status_code != 200:
        logging.error(f"ascii2d color failed:{compress_html(color_content)}")
        return

    results = {'color': parse_ascii2d(color_content, color_resp.url)}
    bovm_url = color_resp.url.replace('/color/', '/bovm/')
    bovm_resp = requests.get(bovm_url)
    bovm_content = bovm_resp.content.decode()

    if bovm_resp.status_code != 200:
        logging.error(f'ascii2d bovm failed:{compress_html(bovm_content)}')
        return results

    results['bovm'] = parse_ascii2d(bovm_content, bovm_url)
    logging.info(f'ascii2d:{json.dumps(results, ensure_ascii=False)}')
    return results


def parse_ascii2d(content, base_url):
    items = BeautifulSoup(content).select('.item-box')
    items.pop(0)
    return [
        {
            'thumbnail': base_url + item.select_one('.image-box > img')['src'],
            'size': item.select_one('.info-box > small').string,
            'sources': [
                {
                    'link': source.contents[1].href,
                    'title': source.contents[1].string,
                    'author': source.contents[2].string,
                    'author_link': source.contents[1].href,
                    'site': source.contents[3].string
                }
                for source in item.select_one('.detail_box > h6')
            ]
        }
        for item in items
    ]


def search_nhentai(file):
    raise NotImplementedError()


def search_whatanime(file):
    raise NotImplementedError()
