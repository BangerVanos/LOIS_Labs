########################
#
# Лабораторная работа № 4 по дисциплине "Логические основы интеллектуальных систем"
# Выполнена студентами группы 121702 БГУИР Заломовом Р.А., Готиным И.А., Булановичем В.И.
# Файл содержит класс, реализующий подготовку данных для проведения прямого нечёткого вывода
# Дата: 25.09.23
#
########################


import regex as re


class FuzzySetParser:
    FUZZY_SET_PATTERN = r'^({(<([a-z]|([a-z][1-9][0-9]*)),((1\.0)|(0\.[0-9]))>)(,(?2))*})$'
    FUZZY_SET_WITH_NAME_PATTERN = r'^([A-Z]|(A-Z[1-9][0-9]*))' \
                                  r'=({(<([a-z]|([a-z][1-9][0-9]*)),((1\.0)|(0\.[0-9]))>)(,(?4))*})$'

    @classmethod
    def parse_fuzzy_set(cls, raw_line: str) -> dict | None:
        if not re.fullmatch(cls.FUZZY_SET_PATTERN, raw_line):
            return None
        raw_line = raw_line[1:-1]
        raw_elements = [element.replace('<', '').replace('>', '') for element in raw_line.split('>,<')]
        elements = {item.split(',')[0]: float(item.split(',')[1]) for item in raw_elements}
        if not raw_line.count('<') == len(elements):
            return None
        return elements

    @classmethod
    def read_file_for_fuzzy_sets(cls, facts_dir: str, premises_dir: str) -> dict | None:
        premises_and_facts = {'premises': {},
                              'facts': {}}
        with open(facts_dir, 'r') as facts_file:
            for line in facts_file:
                line = line.strip('\n')
                if not re.fullmatch(cls.FUZZY_SET_WITH_NAME_PATTERN, line):
                    return None
                fuzzy_set = line.split('=')
                premises_and_facts['facts'][fuzzy_set[0]] = fuzzy_set[1]
        with open(premises_dir, 'r') as premises_file:
            for line in premises_file:
                line = line.strip('\n')
                if not re.fullmatch(cls.FUZZY_SET_WITH_NAME_PATTERN, line):
                    return None
                fuzzy_set = line.split('=')
                premises_and_facts['premises'][fuzzy_set[0]] = fuzzy_set[1]
        return premises_and_facts

    @classmethod
    def parse_read_fuzzy_sets(cls, raw_fuzzy_sets: dict) -> dict | None:
        if not raw_fuzzy_sets.get('premises') or not raw_fuzzy_sets.get('facts'):
            return None
        for name, raw_set in raw_fuzzy_sets['premises'].items():
            raw_fuzzy_sets['premises'][name] = cls.parse_fuzzy_set(raw_set)
        for name, raw_set in raw_fuzzy_sets['facts'].items():
            raw_fuzzy_sets['facts'][name] = cls.parse_fuzzy_set(raw_set)
        return raw_fuzzy_sets
