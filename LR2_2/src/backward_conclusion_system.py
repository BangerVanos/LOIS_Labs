########################
#
# Лабораторная работа № 5 по дисциплине "Логические основы интеллектуальных систем"
# Выполнена студентами группы 121702 БГУИР Заломовым Р.А., Готиным И.А., Булановичем В.И.
# Файл содержит класс, объединяющим парсер и решатель задач системы, реализующей обратный нечёткий логический вывод
# Дата: 25.11.23
#
########################


from .backward_conclusion_solver import BackwardFuzzyConclusionSolver
from .backward_conclusion_parser import BackwardFuzzyConclusionParser
from .additional_math import Interval


class BackwardFuzzyConclusionSystem:
    @classmethod
    def run(cls, file_path: str):
        parsing_result = BackwardFuzzyConclusionParser.parse(file_path)
        solver_result = BackwardFuzzyConclusionSolver.solve(parsing_result)
        printable_strings = cls._stringify_solutions(solver_result)
        for string in printable_strings:
            print(string)

    @classmethod
    def _stringify_solutions(cls, solutions):
        printable_strings = []
        for arguments, solutions in solutions.items():
            solutions_strings = []
            for solution in solutions:
                solutions_strings.append(cls._stringify_solution(solution))
            connected_solutions = f'({"⋃".join(solutions_strings)})'
            conclusion, relation = arguments.split(',')
            printable_strings.append(f'(Relation: {relation}, Conclusion: {conclusion}): '
                                     f'{connected_solutions}')
        return printable_strings

    @classmethod
    def _stringify_solution(cls, solution: dict):
        pairs = []
        for var, membership_degree in solution.items():
            pairs.append(f'<{var},μ({var})∈{membership_degree}>' if isinstance(membership_degree,
                                                                               Interval) else
                         f'<{var},{membership_degree}>')
        return '{' + ','.join(pairs) + '}'
