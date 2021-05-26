import json
import logging

from requests import Response


def dumper(data):
    if isinstance(data, dict):
        return json.dumps(data, ensure_ascii=False)
    return str(data)


def log_service_req_failed(service, res: Response):
    body = res.content.decode()[:100].replace('\n', '\\n')
    logging.info(f'Service {service} failed: Request to {res.url} status code {res.status_code} body {body}')


def log_service_ok(service, ret):
    logging.debug(f'Service {service} ok: Result {dumper(ret)}')
