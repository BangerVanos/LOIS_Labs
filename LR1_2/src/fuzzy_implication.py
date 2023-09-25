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


class FuzzyOutput:

    @staticmethod
    def make_dataframe(fuzzy_set_1: dict, fuzzy_set_2: dict) -> pd.DataFrame:
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
    def fuzzy_conclusion(cls, premise: dict, implication_matrix: pd.DataFrame) -> dict | None:
        conclusion_result = {}
        if list(implication_matrix.index) != list(premise.keys()):
            return None
        for key, value in premise.items():
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
