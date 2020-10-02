import imghdr

import requests
from bs4 import BeautifulSoup

from . import handle_file
from .log import log_error, log_success


@handle_file
def search_ascii2d(file):
    token_resp = requests.get('https://ascii2d.net/')

    if token_resp.status_code != 200:
        log_error('ascii2d request token failed', token_resp)
        return

    token_soup = BeautifulSoup(token_resp.content.decode(), 'html.parser')
    token = token_soup.select_one('input[name="authenticity_token"]')['value']

    filetype = imghdr.what(file)
    file.seek(0)
    if filetype is None:
        log_error('ascii2d check filetype failed', 'unknown filetype')
        return

    color_resp = requests.post('https://ascii2d.net/search/file', {
        'utf8': '✓',
        "authenticity_token": token
    }, files={'file': (f'image.{filetype}', file, f'image/{filetype}')})

    if color_resp.status_code != 200:
        log_error('ascii2d request color failed', color_resp)
        return

    results = {'color': parse_ascii2d_content(color_resp.content.decode(), color_resp.url)}
    bovw_url = color_resp.url.replace('/color/', '/bovw/')
    bovw_resp = requests.get(bovw_url)

    if bovw_resp.status_code != 200:
        log_error('ascii2d request bovw failed', bovw_resp)
        log_success('ascii2d', results)
        return results

    results['bovw'] = parse_ascii2d_content(bovw_resp.content.decode(), bovw_url)
    log_success('ascii2d', results)
    return results


def parse_ascii2d_content(content, base_url):
    items = BeautifulSoup(content, 'html.parser').select('.item-box')
    items.pop(0)

    def parse_link_group(source):
        link_group = [{'name': str(elem.string), 'url': elem['href']} for elem in source.select('a')]
        if source.contents[0].name == 'img':
            link_group = link_group[1:]
        return link_group

    return [
        {
            'thumbnail': base_url + item.select_one('.image-box > img')['src'],
            'hash': str(item.select_one('.info-box > div.hash').string),
            'size': str(item.select_one('.info-box > small').string),
            'links': [parse_link_group(source) for source in item.select('.detail-box > h6')]
        }
        for item in items
    ]
