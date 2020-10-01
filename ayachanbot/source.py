import json
import logging
import imghdr

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
    def compress_html(raw):
        return ' '.join(raw.split())

    token_resp = requests.get('https://ascii2d.net/')
    token_content = token_resp.content.decode()

    if token_resp.status_code != 200:
        logging.error(f"ascii2d failed:{compress_html(token_content)}")
        return

    token_soup = BeautifulSoup(token_content, 'html.parser')
    token = token_soup.select_one('input[name="authenticity_token"]')['value']

    file_type = imghdr.what(file)
    if file_type is None:
        logging.error("ascii2d failed:unknown filetype")
        return
    file.seek(0)

    color_resp = requests.post('https://ascii2d.net/search/file', {
        'utf8': '✓',
        "authenticity_token": token
    }, files={'file': (f'image.{file_type}', file, f'image/{file_type}')})
    color_content = color_resp.content.decode()

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
    items = BeautifulSoup(content, 'html.parser').select('.item-box')
    items.pop(0)

    def parse_link_group(source):
        link_group = [{'name': elem.string, 'url': elem['href']} for elem in source.select('a')]
        if source.contents[0].name == 'img':
            link_group = link_group[1:]
        return link_group

    return [
        {
            'thumbnail': base_url + item.select_one('.image-box > img')['src'],
            'hash': item.select_one('.info-box > div.hash').string,
            'size': item.select_one('.info-box > small').string,
            'links': [parse_link_group(source) for source in item.select('.detail-box > h6')]
        }
        for item in items
    ]


def search_nhentai(file):
    raise NotImplementedError()


def search_whatanime(file):
    raise NotImplementedError()
