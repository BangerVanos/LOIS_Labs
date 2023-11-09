########################
#
# Лабораторная работа № 4 по дисциплине "Логические основы интеллектуальных систем"
# Выполнена студентами группы 121702 БГУИР Заломовом Р.А., Готиным И.А., Булановичем В.И.
# Файл содержит класс, реализующий подготовку данных для проведения прямого нечёткого вывода
# Дата: 25.09.23
#
########################


import regex as re
from dataclasses import dataclass


@dataclass
class FuzzyImplication:
    first_implicant: str
    second_implicant: str


class FuzzySetParser:
    FUZZY_SET_PATTERN = r'^({(<([a-z]|([a-z][1-9][0-9]*)),(0|1|(1\.0)|(0\.[0-9]+))>)(,(?2))*})$'
    FACT_PATTERN = r'^([A-Z]|([A-Z][1-9][0-9]*))=({(<([a-z]|([a-z][1-9][0-9]*)),(0|1|(1\.0)|(0\.[0-9]+))>)(,(?4))*})\.$'
    PREDICATE_PATTERN = r'^([A-Z]|([A-Z][1-9][0-9]*))~>(?1)\.$'

    @classmethod
    def __parse_fuzzy_set(cls, raw_line: str) -> dict | None:
        if not re.fullmatch(cls.FUZZY_SET_PATTERN, raw_line):
            return None
        raw_line = raw_line[1:-1]
        raw_elements = [element.replace('<', '').replace('>', '') for element in raw_line.split('>,<')]
        elements = {item.split(',')[0]: float(item.split(',')[1]) for item in raw_elements}
        if not raw_line.count('<') == len(elements):
            return None
        return elements

    @classmethod
    def __parse_program_file(cls, file_dir: str) -> dict | None:
        parse_result: dict = {'facts': {},
                              'predicates': {}}
        with open(file_dir) as file:
            line_index = 0
            for line in file:
                line_index += 1
                line = line.strip('\n').replace(' ', '').replace('\t', '')
                if re.fullmatch(cls.FACT_PATTERN, line):
                    fact = line.split('=')
                    if fact[0] in parse_result['predicates'].keys():
                        raise ValueError(f'ERROR ON LINE {line_index}: Literal type is Predicate, not Fact')
                    parse_result['facts'][fact[0]] = fact[1][:-1]
                elif re.fullmatch(cls.PREDICATE_PATTERN, line):
                    predicate = line[:-1]
                    if predicate in parse_result['predicates'].keys():
                        raise ValueError(f'ERROR ON LINE {line_index}: Predicate ({predicate}) '
                                         f'presented in program several times.')
                    parse_result['predicates'][predicate] = predicate
                elif line == '':
                    continue
                else:
                    raise ValueError(f'ERROR ON LINE {line_index}: Cannot parse this line')
        return parse_result
    
    @classmethod
    def __parse_program_file_result(cls, raw_parse: dict) -> dict | None:
        for _set in raw_parse['facts'].keys():
            raw_parse['facts'][_set] = cls.__parse_fuzzy_set(raw_parse['facts'][_set])
        for _implication in raw_parse['predicates'].keys():
            raw_parse['predicates'][_implication] = cls.__parse_fuzzy_implication(raw_parse['predicates'][_implication])
        return raw_parse
    
    @classmethod
    def __parse_fuzzy_implication(cls, raw_line: str) -> FuzzyImplication:
        implicants = raw_line.split('~>')
        return FuzzyImplication(implicants[0], implicants[1])

    @classmethod
    def parse(cls, file_dir: str = 'program') -> dict | None:
        raw_parse: dict = cls.__parse_program_file(file_dir)
        return cls.__parse_program_file_result(raw_parse)
