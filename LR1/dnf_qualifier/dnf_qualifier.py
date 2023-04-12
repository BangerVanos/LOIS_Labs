########################
#
# Лабораторная работа № 1 по дисциплине "Логические основы интеллектуальных систем"
# Выполнена студентами группы 121702 БГУИР Заломовом Р.А. и Готиным И.А.
# Файл содержит класс, определяющий, имеет ли строка, содержащая логическую функию, форму ДНФ
# Дата: 27.03.23
# Дата: 11.04.23 v 1.1 Исправлен подход к решению задачи
#
########################


class IncorrectFormula(Exception):
    pass


class DNFQualifier:
    MACHINERY_SYMBOLS = {'disjunction': '|',
                         'conjunction': '&',
                         'negation': '!'}  # Dictionary with logical operations (machinery ones)

    CONSTANTS = ('1', '0')  # Constants list
    ALLOWED_SYMBOLS = 'ABCDEFGHIJKMNLOPQRSTUVWXYZ0123456789\\/()!'

    @classmethod
    def is_dnf(cls, formula: str) -> bool:
        """Method checks if given formula is in DNF form"""
        if not all([sym in cls.ALLOWED_SYMBOLS for sym in formula]):  # Check if all formula's symbols are allowed
            raise IncorrectFormula('Not allowed symbol')
        if cls.__is_variable(formula) and formula not in cls.CONSTANTS:
            return True
        elif formula in cls.CONSTANTS:
            return False
        formula = cls.__replace_special_syms(formula)
        try:
            initial_check = cls.__initial_check(formula)
        except IncorrectFormula as err:
            raise IncorrectFormula(err)
        if not initial_check:
            return False
        operations_rank_list = cls.__apply_ranks_to_operations(formula)
        if not cls.__check_operations_order(operations_rank_list):
            return False
        return True

    @classmethod
    def __initial_check(cls, formula: str):
        """Initial check for formula"""
        if not formula:
            raise IncorrectFormula("Formula string is empty")
        try:
            if not cls.__only_atomic_negations(formula):
                return False
        except IncorrectFormula as err:
            raise IncorrectFormula(err)
        formula_parenthesis = [sym for sym in formula if sym in ('(', ')')]  # Making list of formulas parentheses
        if not cls.__check_parenthesis(formula_parenthesis):  # Check if parentheses order and amount is appropriate
            raise IncorrectFormula('Incorrect placement of parenthesis')
        operator_count = formula.count('!') + formula.count('|') + formula.count('&')
        if not len(formula_parenthesis) == operator_count * 2:
            return False
        try:
            operation_syntax = cls.__check_formula_syntax(formula)
        except IncorrectFormula as err:
            raise IncorrectFormula(err)
        if not operation_syntax:
            return False
        return True

    @staticmethod
    def __check_parenthesis(parenthesis_list: list[str]):
        """Method checks if parenthesis order is correct and whether amount
        of close and open parentheses is the same"""
        parenthesis_stack = []  # Stack method is used
        mapping = {')': '('}
        for parenthesis in parenthesis_list:
            if mapping.get(parenthesis):  # If closing parenthesis is found
                top_element = parenthesis_stack.pop() if parenthesis_stack else '#'  # first element of stack is got
                if mapping[parenthesis] != top_element:  # If stack's top element is not opening parenthesis
                    return False  # the sequence of parentheses is not right
            else:
                parenthesis_stack.append(parenthesis)
        return not parenthesis_stack  # If parentheses stack is not empty, sequence of parentheses is not right

    @classmethod
    def __only_atomic_negations(cls, formula: str):
        """Method check whether negations in formula are used only for atomic formulas"""
        while not formula.find('!') == -1:
            negation_index = formula.find('!')
            try:
                negation_subformula = formula[negation_index + 1:formula.find(')', negation_index)]
            except IndexError:
                raise IncorrectFormula('No closing parenthesis')
            if not cls.__is_variable(negation_subformula):
                return False
            formula = formula.replace(f'!{negation_subformula}', '', 1)
        return True

    @staticmethod
    def __replace_special_syms(formula: str):
        """Replace some operation symbols for better processing"""
        return formula.replace('\\/', '|').replace('/\\', '&')

    @classmethod
    def __apply_ranks_to_operations(cls, formula: str):
        """Method applies ranks for formula operations"""
        operation_rank = 0
        operations_rank_list = []
        for sym in formula:
            if sym == '(':
                operation_rank += 1
            elif sym == ')':
                operation_rank -= 1
            elif sym in cls.MACHINERY_SYMBOLS.values() and sym != cls.MACHINERY_SYMBOLS['negation']:
                operations_rank_list.append((sym, operation_rank))
        return sorted(operations_rank_list, key=lambda x: x[1])

    @classmethod
    def __check_operations_order(cls, operations_rank_list: list):
        """Method checks whether operation order matches that one for DNF"""
        last_operation = (None, None)
        for operation_rank in operations_rank_list:
            if (operation_rank[0] == cls.MACHINERY_SYMBOLS['disjunction']
                and last_operation[0] == cls.MACHINERY_SYMBOLS['conjunction']) \
                    and (operation_rank[1] != last_operation[1]):
                return False
            last_operation = operation_rank
        return True

    @classmethod
    def __is_variable(cls, variable: str):
        """Method checks whether string is variable"""
        if not variable:
            raise IncorrectFormula('Empty variable')
        if not variable[0].isupper():  # Variable's name can only contain upper latin letters with optional index
            return False
        if len(variable) > 1:  # If variable's name contains index
            if not (variable[1:].isdigit() and not variable[1] == '0'):  # Index can only be natural number
                return False
        return True

    @classmethod
    def __check_formula_syntax(cls, formula: str):
        """Method checks if formula matches boolean algebra formula syntax"""
        while not formula == '#':
            deepest_operation_index = cls.__find_index_of_deepest_operation(formula)
            close_parenthesis_index = formula[deepest_operation_index:].find(')') + deepest_operation_index
            if close_parenthesis_index == -1:
                raise IncorrectFormula('No close parenthesis')
            open_parenthesis_index = formula[:deepest_operation_index].rfind('(')
            if formula[deepest_operation_index] == cls.MACHINERY_SYMBOLS['negation']:
                negation_argument = formula[deepest_operation_index + 1:close_parenthesis_index]
                if not (deepest_operation_index - open_parenthesis_index == 1 and (cls.__is_variable(negation_argument)
                                                                                   or negation_argument == '#')):
                    raise IncorrectFormula('Incorrect negation argument')
            else:
                left_argument = formula[open_parenthesis_index + 1:deepest_operation_index]
                right_argument = formula[deepest_operation_index + 1:close_parenthesis_index]
                if not ((cls.__is_variable(left_argument) or left_argument == '#')
                        and (cls.__is_variable(right_argument) or right_argument == '#')):
                    raise IncorrectFormula('Incorrect binary operation arguments')
            formula = formula[:open_parenthesis_index] + '#' + formula[close_parenthesis_index + 1:]
        return True

    @classmethod
    def __find_index_of_deepest_operation(cls, formula: str):
        """Method finds 'deepest' operation in formula and returns its index"""
        deepest_parenthesis_index = formula.rfind('(')
        for i in range(deepest_parenthesis_index, len(formula)):
            if formula[i] in cls.MACHINERY_SYMBOLS.values():
                return i
        raise IncorrectFormula('Incorrect formula')
