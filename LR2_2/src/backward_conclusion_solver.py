########################
#
# Лабораторная работа № 5 по дисциплине "Логические основы интеллектуальных систем"
# Выполнена студентами группы 121702 БГУИР Заломовым Р.А., Готиным И.А., Булановичем В.И.
# Файл содержит класс, являющийся решателем задач системы, реализующей обратный нечёткий логический вывод
# Дата: 25.11.23
#
########################


import pandas as pd
from .additional_math import CompositionEquation
from itertools import product
from .additional_math import Interval, AbstractInterval, EmptyInterval


class BackwardFuzzyConclusionSolver:
    @classmethod
    def solve(cls, parse_result: dict):
        equations_dict = cls._make_equations(parse_result)
        equations_dict = cls._find_solutions(equations_dict)
        equations_dict = {system_name: system if None not in system else [] for system_name, system in
                          equations_dict.items()}
        equations_dict = {system_name: list(product(*system)) for system_name, system in equations_dict.items()}
        equations_dict_solutions = cls._unite_solutions(equations_dict)
        equations_dict_solutions = {system: solutions for system, solutions in equations_dict_solutions.items()
                                    if len(solutions) > 0}
        equations_dict_solutions = cls._drop_duplicated_solutions_from_systems(equations_dict_solutions)
        return equations_dict_solutions

    @classmethod
    def _make_equations(cls, parse_result) -> dict[str, list[CompositionEquation]]:
        equations_dict = dict()
        for fact in parse_result['facts']:
            for relation in parse_result['rules']:
                predicate = parse_result['facts'][fact]
                matrix = parse_result['rules'][relation]
                if list(predicate.keys()) != matrix.columns.tolist():
                    continue
                equations_dict[f'{fact},{relation}'] = cls._make_equation_list_for_predicate_and_matrix(
                    predicate, matrix
                )
        equations_dict = {key: value for key, value in equations_dict.items() if value is not None}
        return equations_dict

    @classmethod
    def _make_equation_list_for_predicate_and_matrix(cls, predicate, matrix: pd.DataFrame) -> list[CompositionEquation]:
        equations = []
        for variable in predicate:
            equations.append(CompositionEquation(dict(zip(matrix.index.tolist(),
                                                          list(map(float, matrix.loc[:, variable].tolist())))),
                                                 predicate[variable]))
        return equations

    @classmethod
    def _find_solutions(cls, equations_dict: dict[str, list[CompositionEquation]]):
        return {system_name: list(map(lambda equation: equation.get_solutions_list(), system)) for
                system_name, system in equations_dict.items()}

    @classmethod
    def _unite_solutions(cls, equations_dict):
        all_solutions: dict[str, list] = dict()
        for system_name, possible_solutions in equations_dict.items():
            all_solutions[system_name] = []
            for equation_system in possible_solutions:
                all_solutions[system_name].append(cls._unite_solution(equation_system))
            all_solutions[system_name] = list(filter(lambda x: x is not None, all_solutions[system_name]))
        return all_solutions

    @classmethod
    def _unite_solution(cls, equation_system):
        variables_values: dict[str, list] = dict()
        for equation in equation_system:
            for variable in equation:
                if variables_values.get(variable, None) is None:
                    variables_values[variable] = [equation[variable]]
                else:
                    variables_values[variable].append(equation[variable])
        solution = {var: cls._find_solution_for_variable(values) for var, values in variables_values.items()}
        if None in solution.values():
            return None
        else:
            return solution

    @classmethod
    def _find_solution_for_variable(cls, variable_values):
        if all([isinstance(value, AbstractInterval) for value in variable_values]):
            result_interval = sum(variable_values, Interval(0.0, 1.0))
            if isinstance(result_interval, EmptyInterval):
                return None
            else:
                return result_interval
        numeric_values = set()
        for value in variable_values:
            if isinstance(value, float | int):
                numeric_values.add(value)
        if len(numeric_values) > 1:
            return None
        numeric_value = list(numeric_values)[0]
        variable_intervals = list(filter(lambda x: not isinstance(x, float | int), variable_values))
        if all([numeric_value in interval for interval in variable_intervals]):
            return numeric_value
        else:
            return None

    @classmethod
    def _drop_duplicated_solutions_from_systems(cls, systems_solutions_dict: dict):
        for system_name, system in systems_solutions_dict.items():
            solutions_without_duplicates = []
            [solutions_without_duplicates.append(solution) for solution in system if solution
             not in solutions_without_duplicates]
            unique_solutions = []
            for solution in solutions_without_duplicates:
                if not cls._is_there_more_general_solutions(solution, solutions_without_duplicates):
                    unique_solutions.append(solution)
            systems_solutions_dict[system_name] = unique_solutions
        return systems_solutions_dict

    @classmethod
    def _check_solution_for_inclusion_in_other(cls, solution: dict, other_solution: dict) -> bool:
        # False is returned because it is considered that we won't have same solutions at this moment
        if solution == other_solution:
            return False
        vars_inbounds = set()
        for var in solution.keys():
            if not other_solution.get(var):
                return False
            if isinstance(solution[var], float | int) and isinstance(other_solution[var], float | int) and \
                    solution[var] == other_solution[var]:
                vars_inbounds.add(var)
            elif isinstance(other_solution[var], AbstractInterval) and solution[var] in other_solution[var]:
                vars_inbounds.add(var)
        return vars_inbounds == set(solution.keys())

    @classmethod
    def _is_there_more_general_solutions(cls, solution: dict, solutions_list: list[dict]) -> bool:
        for other_solution in solutions_list:
            if cls._check_solution_for_inclusion_in_other(solution, other_solution):
                return True
        return False
