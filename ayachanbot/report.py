import yaml


class Report:
    def __init__(self):
        self.saucenao_results = None
        self.ascii2d_results = None

    def set_saucenao_results(self, results):
        self.saucenao_results = results
        return self

    def set_ascii2d_results(self, results):
        self.ascii2d_results = results
        return self

    def gen_report(self):
        saucenao_limit = 1
        ascii2d_color_limit = 1
        ascii2d_bovm_limit = 1

        texts = []
        sep = '-' * 80

        def dumps(d):
            return yaml.dump(d, allow_unicode=True)

        if self.saucenao_results:
            text = f"SauceNAO results:\n{sep}\n"
            for result in self.saucenao_results[:saucenao_limit]:
                text += f"{dumps(result['header'])}\n{dumps(result['data'])}{sep}\n"
            texts.append(text)

        if self.ascii2d_results:
            def display_link(link):
                return f"{link['name']}: {link['url']}" if link['url'] else link['name']

            def preprocess_results(res_list):
                for res in res_list:
                    res['links'] = [[display_link(link) for link in link_group] for link_group in res['links']]
                return res_list

            if self.ascii2d_results.get('color', None):
                text = f'ascii2d color results:\n{sep}\n'
                results = self.ascii2d_results['color'][:ascii2d_color_limit]
                results = preprocess_results(results)
                for result in results:
                    text += f"{dumps(result)}{sep}\n"

            if self.ascii2d_results.get('bovm', None):
                text = f'ascii2d feature results:\n{sep}\n'
                results = self.ascii2d_results['bovm'][:ascii2d_bovm_limit]
                results = preprocess_results(results)
                for result in results:
                    text += f"{dumps(result)}{sep}\n"

        text = f"{sep}\n{sum(texts, '')}"
        return text
