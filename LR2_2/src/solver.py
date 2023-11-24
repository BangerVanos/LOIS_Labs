import numpy as np
import pandas as pd
from sympy import Interval
from collections import defaultdict
from decimal import Decimal, getcontext
getcontext().prec = 8


class Solver:
    @staticmethod
    def __check_fact_in_rule(rule: pd.DataFrame, fact: dict) -> bool:
        for key in fact.keys():
            if key not in rule.index.tolist() + rule.columns.tolist():
                return True
        return False

    @staticmethod
    def __find_interval_intersections(data):
        variables = set()
        intervals = {}

        for item in data:
            for var, interval in item.items():
                variables.add(var)
                if var in intervals:
                    intervals[var] = intervals[var].intersect(interval)
                else:
                    intervals[var] = interval

        result = {var: intervals[var] for var in sorted(variables)}
        return result

    @staticmethod
    def solve(result: dict):
        for rule_name, rule in result['rules'].items():
            solutions = defaultdict(dict)
            for fact_name in result['facts']:
                if len(rule.index) != len(result['facts'][fact_name]):
                    break
                for index_eq, target_value in enumerate(result['facts'][fact_name].values()):
                    equation = rule.iloc[index_eq].to_numpy()
                    for i, variable in enumerate(equation):
                        variable = float(variable)
                        if variable == 0:
                            continue
                        ai = target_value / variable
                        if 0 < ai <= 1:
                            solutions[index_eq][f'y{i + 1}'] = Interval(0, ai)

                intervals = Solver.__find_interval_intersections(solutions.values())
                if len(intervals) != len(rule.columns):
                    raise ValueError('Empty Interval')

                if not Solver.__final_check(intervals, rule, result['facts'][fact_name]):
                    print('Impossible to solve')
                    exit()
                return intervals

    @staticmethod
    def __final_check(intervals: dict, rule: pd.DataFrame, vector: dict) -> bool:
        intervals = list(intervals.values())
        vector = list(vector.values())
        for i in range(len(rule.index)):
            result = []
            for j in range(len(rule.columns)):
                result.append(Decimal(rule.iloc[i, j]) * Decimal(str(intervals[j].end)))

            result = float(max(result))
            if result != vector[i]:
                return False
        return True
