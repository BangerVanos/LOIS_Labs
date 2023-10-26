########################
#
# Лабораторная работа № 4 по дисциплине "Логические основы интеллектуальных систем"
# Выполнена студентами группы 121702 БГУИР Заломовом Р.А., Готиным И.А., Булановичем В.И.
# Файл содержит класс, собирающий все компоненты системы воедино
# Дата: 25.09.23
# Дата: 26.10.23 Добавлено отслеживание исключений
#
########################


from src.fuzzy_implication import FuzzyConclusionSolver
from src.fuzzy_set_parser import FuzzySetParser
import sys


class FuzzyImplicationSystem:

    @classmethod
    def __get_all_conclusions(cls, program_file: str) -> list:
        try:
            parse_result = FuzzySetParser.parse(program_file)
        except ValueError as err:
            print(err)
            print('Fix error on that line and come again')
            sys.exit(-1)
        solve_result = FuzzyConclusionSolver.solve(parse_result)
        return solve_result

    @classmethod
    def print_conclusions_results(cls, program_file: str):
        conclusions = cls.__get_all_conclusions(program_file)
        print('All possible conclusions results:')
        for conclusion in conclusions:
            conclusion_str = f'{conclusion.conclusion_level}.{conclusion.premises}' \
                             f'|-{cls.fuzzy_set_dict_to_str(conclusion.conclusion)}' \
                             f'={conclusion.result_name}'
            print('\t'*(conclusion.conclusion_level - 1)+f'|-{conclusion_str}')

    @staticmethod
    def fuzzy_set_dict_to_str(conclusion_result: dict | None) -> str | None:
        if conclusion_result is None:
            return None
        text = '{'
        for key, value in conclusion_result.items():
            text += f'<{key},{value}>'
            text += ','
        else:
            text = text[:-1]
            text += '}'
        return text
