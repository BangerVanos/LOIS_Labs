########################
#
# Лабораторная работа № 4 по дисциплине "Логические основы интеллектуальных систем"
# Выполнена студентами группы 121702 БГУИР Заломовом Р.А., Готиным И.А., Булановичем В.И.
# Файл класс, реализующий прямой нечёткий вывод для обработанных данных
# Дата: 25.09.23
# Дата: 10.10.23 изменён метод поиска точной верхней грани
#
########################


import pandas as pd
from dataclasses import dataclass


@dataclass
class FuzzyConclusion:
    conclusion_level: int | None
    premises: str | None
    conclusion: str | None


class FuzzyConclusionSolver:

    @staticmethod
    def __gauguin_norm_delta(f_belonging_degree: int | float, s_belonging_degree: int | float) -> float:
        if f_belonging_degree <= s_belonging_degree:
            return 1.0
        else:
            return s_belonging_degree / f_belonging_degree

    @classmethod
    def __fuzzy_implication(cls, fuzzy_set_1: dict, fuzzy_set_2: dict) -> pd.DataFrame:
        df = pd.DataFrame(columns=fuzzy_set_2.keys(), index=fuzzy_set_1.keys())
        for key_2, value_2 in fuzzy_set_2.items():
            for key_1, value_1 in fuzzy_set_1.items():
                solution = cls.__gauguin_norm_delta(value_1, value_2)
                df.loc[key_1, key_2] = solution
        return df

    @classmethod
    def __fuzzy_conclusion(cls, fact: dict, implication_matrix: pd.DataFrame) -> dict | None:
        conclusion_result = {}
        result_implication_matrix = pd.DataFrame(index=implication_matrix.index, columns=implication_matrix.columns)
        if list(implication_matrix.index) != list(fact.keys()):
            return None
        for key, value in fact.items():
            result_implication_matrix.loc[key] = implication_matrix.loc[key] * value
        for key in implication_matrix.columns:
            conclusion_result[key] = max(result_implication_matrix.loc[:, key])
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
            second_fact = parse_result['facts'].get(implication.second_implicant)
            parse_result['predicates'][predicate] = cls.__fuzzy_implication(first_fact, second_fact)
        return parse_result

    @classmethod
    def solve(cls, parse_result: dict) -> list[FuzzyConclusion] | None:

        solver_results = list()
        facts_and_predicates = cls.__solve_implications(parse_result)
        all_predicates_used = False
        used_predicates_by_level = {0: set()}
        solve_level = 1
        new_fact_index = 0

        while not all_predicates_used:
            conclusion_results = []
            used_predicates_by_level[solve_level] = set()
            for fact in facts_and_predicates['facts']:
                for predicate in facts_and_predicates['predicates']:
                    if predicate in used_predicates_by_level[solve_level - 1] or fact in predicate:
                        continue
                    premises = '{' + ','.join([fact, '(' + predicate + ')']) + '}'
                    conclusion_result = cls.__fuzzy_conclusion(facts_and_predicates['facts'][fact],
                                                               facts_and_predicates['predicates'][predicate])
                    if conclusion_result is not None:
                        conclusion_results.append(FuzzyConclusion(solve_level, premises,
                                                                  cls.fuzzy_set_dict_to_str(conclusion_result)))
                        used_predicates_by_level[solve_level].add(predicate)
            for conclusion_result in conclusion_results:
                if conclusion_result.conclusion is not None:
                    new_fact_index += 1
                    facts_and_predicates['facts'][f'P#{new_fact_index}'] = conclusion_result.conclusion
                    solver_results.append(conclusion_result)
            if len(used_predicates_by_level[solve_level]) <= 0:
                all_predicates_used = True
            solve_level += 1
        return solver_results
