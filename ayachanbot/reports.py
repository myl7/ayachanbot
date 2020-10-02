import yaml

SEP = '-' * 80


def handle_none(f):
    def wrapper(results):
        if not results:
            return ''
        return f(results)

    return wrapper


@handle_none
def report_saucenao(results):
    saucenao_limit = 1

    text = f'{SEP}\nSauceNAO results:\n{SEP}\n'
    for result in results[:saucenao_limit]:
        text += f"{dumps(result['header'])}\n{dumps(result['data'])}{SEP}\n"
    yield text


@handle_none
def report_ascii2d(ascii2d_results):
    ascii2d_color_limit = 1
    ascii2d_bovw_limit = 1

    def display_link(link):
        return f"{link['name']}: {link['url']}" if link['url'] else link['name']

    def preprocess_results(res_list):
        for res in res_list:
            res['links'] = [[display_link(link) for link in link_group] for link_group in res['links']]
        return res_list

    if ascii2d_results.get('color', None):
        text = f'{SEP}\nascii2d color results:\n{SEP}\n'
        results = ascii2d_results['color'][:ascii2d_color_limit]
        results = preprocess_results(results)
        for result in results:
            text += f'{dumps(result)}{SEP}\n'
        yield text

    if ascii2d_results.get('bovw', None):
        text = f'{SEP}\nascii2d feature results:\n{SEP}\n'
        results = ascii2d_results['bovw'][:ascii2d_bovw_limit]
        results = preprocess_results(results)
        for result in results:
            text += f'{dumps(result)}{SEP}\n'
        yield text


@handle_none
def report_whatanime(results):
    whatanime_limit = 1

    text = f'{SEP}\nwhatanime results:\n{SEP}\n'
    results = results['docs'][:whatanime_limit]
    for result in results:
        text += f'{dumps(result)}{SEP}\n'
    yield text


def dumps(d):
    return yaml.safe_dump(d, allow_unicode=True)
