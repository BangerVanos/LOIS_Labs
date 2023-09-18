import regex as re


class FuzzySetParser:
    FUZZY_SET_PATTERN = r'^({(<([a-z]|([a-z][1-9][0-9]*)),((1\.0)|(0\.[0-9]))>)(,(?2))*})$'

    @classmethod
    def parse_fuzzy_set(cls, raw_line: str) -> dict | None:
        if not re.fullmatch(cls.FUZZY_SET_PATTERN, raw_line):
            return None
        raw_line = raw_line[1:-1]
        raw_elements = [element.replace('<', '').replace('>', '') for element in raw_line.split('>,<')]
        elements = {item.split(',')[0]: float(item.split(',')[1]) for item in raw_elements}
        if not raw_elements.count('<') == len(elements):
            return None
        return elements
