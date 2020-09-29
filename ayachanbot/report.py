import yaml


class Report:
    def __init__(self):
        self.saucenao_results = []

    def set_saucenao_results(self, results):
        self.saucenao_results = results
        return self

    def gen_report(self):
        texts = []

        if self.saucenao_results:
            def dumper(result, section):
                return yaml.dump(result[section], allow_unicode=True)

            sep = '-' * 80
            text = f"{sep}SauceNAO results:\n{sep}\n"
            limit = 1
            for result in self.saucenao_results[:limit]:
                text += f"{dumper(result, 'header')}\n{dumper(result, 'data')}{sep}"
            texts.append(text)

        return texts
