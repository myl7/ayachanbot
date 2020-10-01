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
        texts = []
        sep = f"\n{'-' * 80}\n"

        if self.saucenao_results:
            def dumper(res, section):
                return yaml.dump(res[section], allow_unicode=True)

            text = f"SauceNAO results:{sep}"
            saucenao_limit = 1
            for result in self.saucenao_results[:saucenao_limit]:
                text += f"{dumper(result, 'header')}\n{dumper(result, 'data')}"[:-1]
            texts.append(text)

        if self.ascii2d_results:
            text = f'ascii2d results:{sep}'

            ascii2d_color_results = self.ascii2d_results['color']
            # noinspection PyUnusedLocal
            ascii2d_color_limit = 1
            ascii2d_color_results.update(ascii2d_color_results['sources'][0])
            text += f'ascii2d color results:\n{yaml.dump(ascii2d_color_results, allow_unicode=True)}\n'

            ascii2d_bovm_results = self.ascii2d_results['bovm']
            # noinspection PyUnusedLocal
            ascii2d_bovm_limit = 1
            ascii2d_bovm_results.update(ascii2d_bovm_results['sources'][0])
            text += f'ascii2d bovm results:\n{yaml.dump(ascii2d_bovm_results, allow_unicode=True)}'[:-1]

        text = f"{'-' * 80}\n{sep.join(texts)}{'-' * 80}"
        return text
