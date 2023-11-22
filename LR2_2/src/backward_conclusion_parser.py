import pandas as pd
import regex as re
import numpy as np


class BackwardConclusionParser:
    FACT_PATTERN = r'^([A-Z]|([A-Z][1-9][0-9]*))=({(<([a-z]|([a-z][1-9][0-9]*)),(0|1|(1\.0)|(0\.[0-9]+))>)(,(?4))*})\.$'
    RULE_PATTERN = r'^([A-Z]|([A-Z][1-9][0-9]*))=({(<<([a-z]|([a-z][1-9][0-9]*)),([a-z]|([a-z][1-9][0-9]*))>,' \
                   r'(0|1|(1\.0)|(0\.[0-9]+))>)(,(?4))*})\.$'

    @classmethod
    def _parse_program_file(cls, file):
        parse_result = {'facts': {}, 'rules': {}}
        with open(file, 'r') as file:
            for line_index, line in enumerate(file.readlines()):
                line = line.strip('\n').replace('\t', '').replace(' ', '')
                if re.fullmatch(cls.FACT_PATTERN, line):
                    fact_name, fact = line.split('=')
                    if fact_name in parse_result['rules']:
                        raise ValueError(f'ERROR ON LINE {line_index + 1}: {fact_name} has type '
                                         f'\'Fuzzy binary predicate\', not \'Fuzzy predicate\'.')
                    parse_result['facts'][fact_name] = fact[:-1]
                elif re.fullmatch(cls.RULE_PATTERN, line):
                    rule_name, rule = line.split('=')
                    if rule_name in parse_result['facts']:
                        raise ValueError(f'ERROR ON LINE {line_index + 1}: {rule_name} has type \'Fuzzy predicate\','
                                         f' not \'Fuzzy binary predicate\'.')
                    parse_result['rules'][rule_name] = rule[:-1]
                elif line == '':
                    continue
                else:
                    raise ValueError(f'ERROR ON LINE {line_index + 1}: cannot parse this line.')
        return parse_result

    @staticmethod
    def _parse_fuzzy_predicate(raw_predicate: str) -> dict[str, float] | None:
        raw_predicate = raw_predicate[1:-1]
        raw_elements = [element.replace('<', '').replace('>', '') for element in raw_predicate.split('>,<')]
        elements: dict[str, float] = {item.split(',')[0]: float(item.split(',')[1]) for item in raw_elements}
        return elements

    @staticmethod
    def _parse_fuzzy_binary_predicate(raw_predicate: str) -> pd.DataFrame | None:
        raw_predicate = raw_predicate[1:-1]
        relationship_matrix = pd.DataFrame()

        for symbol in raw_predicate.split('>,<'):
            symbol = symbol.replace('>', '').replace('<', '')
            first_element, second_element, membership_degree = symbol.split(',')
            relationship_matrix.loc[first_element, second_element] = membership_degree
        relationship_matrix.replace('n', np.nan, inplace=True)
        relationship_matrix.fillna(0, inplace=True)
        return relationship_matrix

    @classmethod
    def _parse_raw_result(cls, raw_result: dict[str, dict[str, str]]) -> dict | None:
        for fact in raw_result['facts']:
            raw_result['facts'][fact] = cls._parse_fuzzy_predicate(raw_result['facts'][fact])
        for rule in raw_result['rules']:
            raw_result['rules'][rule] = cls._parse_fuzzy_binary_predicate(raw_result['rules'][rule])
        return raw_result

    @classmethod
    def parse(cls, file: str):
        result = cls._parse_program_file(file)
        return cls._parse_raw_result(result)
