########################
#
# Лабораторная работа № 5 по дисциплине "Логические основы интеллектуальных систем"
# Выполнена студентами группы 121702 БГУИР Заломовым Р.А., Готиным И.А., Булановичем В.И.
# Файл содержит классы, обеспечивающие работу с данными, необходимыми для решения задачи обратного нечёткого логического
# вывода
# Дата: 25.11.23
#
########################


from abc import ABC, abstractmethod


class AbstractInterval(ABC):
    @abstractmethod
    def __contains__(self, item):
        pass

    @abstractmethod
    def __add__(self, other):
        pass


class Interval(AbstractInterval):
    _BOUNDARY_RULES = {
        False: [True, False],
        True: [True]
    }

    def __init__(self, left: float | int = 0, right: float | int = 0, strict_left: bool = False,
                 strict_right: bool = False):
        if right < left:
            raise ValueError('Left side cannot be bigger than right one')
        self.left: float | int = left
        self.right: float | int = right
        self.strict_left: bool = strict_left
        self.strict_right: bool = strict_right

    def __contains__(self, item: float | int):
        if not isinstance(item, float | int | AbstractInterval):
            raise TypeError('Intervals can only contain numeric types or other intervals')
        if isinstance(item, float | int):
            return (item > self.left if self.strict_left else item >= self.left) and \
                (item < self.right if self.strict_right else item <= self.right)
        elif isinstance(item, EmptyInterval):
            return True
        elif isinstance(item, Interval):
            containing_score = 0
            if self.left >= item.left:
                containing_score += 1
            if self.right <= item.right:
                containing_score += 1
            if item.strict_right in self._BOUNDARY_RULES[self.strict_right]:
                containing_score += 1
            if item.strict_left in self._BOUNDARY_RULES[self.strict_left]:
                containing_score += 1
            return containing_score == 4
        return False

    def __repr__(self):
        open_bracket = '(' if self.strict_left else '['
        close_bracket = ')' if self.strict_right else ']'
        return f'{open_bracket}{self.left};{self.right}{close_bracket}'

    def __str__(self):
        return self.__repr__()

    def __add__(self, other):
        if not isinstance(other, AbstractInterval):
            raise TypeError(f'Can add only instances of AbstractInterval type, but {type(other)} was provide.')
        if isinstance(other, EmptyInterval):
            return EmptyInterval()
        elif other.__getattribute__('right') < self.left or self.right < other.__getattribute__('left'):
            return EmptyInterval()
        elif other.__getattribute__('right') == self.right and other.__getattribute__('left') == self.left and \
                (self.strict_left or other.__getattribute__('strict_left')
                 or self.strict_right or other.__getattribute__('strict_right')):
            return EmptyInterval()
        else:
            new_left = max(self.left, other.__getattribute__('left'))
            new_right = min(self.right, other.__getattribute__('right'))
            if self.left > other.__getattribute__('left'):
                new_strict_left = self.strict_left
            elif self.left < other.__getattribute__('left'):
                new_strict_left = other.__getattribute__('strict_left')
            else:
                new_strict_left = any([self.strict_left, other.__getattribute__('strict_left')])
            if self.right < other.__getattribute__('right'):
                new_strict_right = self.strict_right
            elif self.left > other.__getattribute__('right'):
                new_strict_right = other.__getattribute__('strict_right')
            else:
                new_strict_right = any([self.strict_left, other.__getattribute__('strict_left')])
            return Interval(new_left, new_right, new_strict_left, new_strict_right)

    def __eq__(self, other):
        if not isinstance(other, Interval):
            return False
        return other.strict_left == self.strict_left and other.strict_right == self.strict_right\
            and other.left == self.left and other.right == self.right


class EmptyInterval(AbstractInterval):
    def __repr__(self):
        return '()'

    def __str__(self):
        return self.__repr__()

    def __add__(self, other):
        if not isinstance(other, AbstractInterval) and not isinstance(other, Interval):
            raise TypeError(f'Can add only instances of AbstractInterval type, but {type(other)} was provide.')
        return EmptyInterval()

    def __contains__(self, item):
        if not isinstance(item, float | int | AbstractInterval):
            raise TypeError('Intervals can only contain numeric types or other intervals')
        return False


class CompositionEquation:
    def __init__(self, expression: dict[str, float | int], result: float | int):
        self.expression = expression
        self.result = result

    def __repr__(self):
        return f'{self.expression} = {self.result}'

    def __str__(self):
        return self.__repr__()

    def get_solutions_list(self):
        possible_fixed_vars = [var for var in self.expression if self.expression[var] >= self.result]
        if len(possible_fixed_vars) <= 0:
            return None
        solutions_list = []
        for fixed_var in possible_fixed_vars:
            solutions_list.append({var: Interval(0, min(1.0, 1.0 if self.expression[var] == 0
                                  else self.result / self.expression[var])) if var != fixed_var
                                  else self.result / self.expression[var]
                                  for var in self.expression})
        unique_solutions = []
        [unique_solutions.append(solution) for solution in solutions_list if solution not in unique_solutions]
        return unique_solutions

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError(f'You can compare {type(self)} object to the same type object')
        return other.result == self.result and other.expression == self.expression
