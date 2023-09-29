########################
#
# Лабораторная работа № 4 по дисциплине "Логические основы интеллектуальных систем"
# Выполнена студентами группы 121702 БГУИР Заломовом Р.А., Готиным И.А., Булановичем В.И.
# Файл класс, реализующий прямой нечёткий вывод для обработанных данных
# Дата: 25.09.23
#
########################


import sympy as sp
import pandas as pd
from dataclasses import dataclass


@dataclass
class FuzzyConclusion:
    premises: str | None
    conclusion: str | None


class FuzzyConclusionSolver:

    @staticmethod
    def __fuzzy_implication(fuzzy_set_1: dict, fuzzy_set_2: dict) -> pd.DataFrame:
        x = sp.symbols('x')
        df = pd.DataFrame(columns=fuzzy_set_2.keys(), index=fuzzy_set_1.keys())
        for key_2, value_2 in fuzzy_set_2.items():
            for key_1, value_1 in fuzzy_set_1.items():
                inequality1 = value_1 * x <= value_2
                inequality2 = x <= 1
                solution = sp.solve_univariate_inequality(inequality1, x,
                                                          relational=False) & sp.solve_univariate_inequality(
                    inequality2, x, relational=False)
                solution = solution.end
                df.loc[key_1, key_2] = solution
        return df

    @classmethod
    def __fuzzy_conclusion(cls, fact: dict, implication_matrix: pd.DataFrame) -> dict | None:
        conclusion_result = {}
        if list(implication_matrix.index) != list(fact.keys()):
            return None
        for key, value in fact.items():
            implication_matrix.loc[key] = implication_matrix.loc[key] * value
        for key in implication_matrix.columns:
            conclusion_result[key] = max(implication_matrix.loc[:, key])
        return conclusion_result

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

    @classmethod
    def __solve_implications(cls, parse_result: dict) -> dict | None:
        for predicate in parse_result['predicates']:
            implication = parse_result['predicates'][predicate]
            first_fact = parse_result['facts'].get(implication.first_implicant)
            second_fact = parse_result['facts'].get(implication.first_implicant)
            parse_result['predicates'][predicate] = cls.__fuzzy_implication(first_fact, second_fact)
        return parse_result

    @classmethod
    def solve(cls, parse_result: dict) -> list[FuzzyConclusion] | None:
        solver_results = list()
        parse_result = cls.__solve_implications(parse_result)
        for fact in parse_result['facts']:
            for predicate in parse_result['predicates']:
                premises = '{' + ','.join([fact, predicate]) + '}'
                conclusion_result = cls.__fuzzy_conclusion(parse_result['facts'][fact],
                                                           parse_result['predicates'][predicate])
                if conclusion_result is not None:
                    solver_results.append(FuzzyConclusion(premises, cls.fuzzy_set_dict_to_str(conclusion_result)))
        return solver_results
