########################
#
# Лабораторная работа № 1 по дисциплине "Логические основы интеллектуальных систем"
# Выполнена студентами группы 121702 БГУИР Заломовом Р.А. и Готиным И.А.
# Файл содержит класс, определяющий, имеет ли строка, содержащая логическую функию, форму ДНФ
# Дата: 27.03.23
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
        if cls.__is_atomic(formula) and formula not in cls.CONSTANTS:
            return True
        elif formula in cls.CONSTANTS:
            return False
        formula = cls.__replace_special_syms(formula)
        try:
            initial_check = cls.__check_initial_check(formula)
        except IncorrectFormula as err:
            raise IncorrectFormula(err)
        if not initial_check:
            return False
        operations_rank_list = cls.__apply_ranks_to_operations(formula)
        if not cls.__check_operations_order(operations_rank_list):
            return False
        return True

    @classmethod
    def __check_initial_check(cls, formula: str):
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
        while not formula.find('!') == -1:
            negation_index = formula.find('!')
            try:
                negation_subformula = formula[negation_index + 1:formula.find(')', negation_index)]
            except IndexError:
                raise IncorrectFormula('No closing parenthesis')
            if not cls.__is_atomic(negation_subformula):
                return False
            formula = formula.replace(f'!{negation_subformula}', '', 1)
        return True

    @staticmethod
    def __replace_special_syms(formula: str):
        """Replace some operation symbols for better processing"""
        return formula.replace('\\/', '|').replace('/\\', '&')

    @classmethod
    def __apply_ranks_to_operations(cls, formula: str):
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
        last_operation = (None, None)
        for operation_rank in operations_rank_list:
            if (operation_rank[0] == cls.MACHINERY_SYMBOLS['disjunction']
                and last_operation[0] == cls.MACHINERY_SYMBOLS['conjunction']) \
                    and (operation_rank[1] != last_operation[1]):
                return False
            last_operation = operation_rank
        return True

    @classmethod
    def __is_atomic(cls, atomic: str):
        """Method checks whether string is atomic formula"""
        if not atomic:
            raise IncorrectFormula('Empty atomic formula')
        if atomic in cls.CONSTANTS:  # Sometimes literal can be constant
            return True
        if not atomic[0].isupper():  # Variable's name can only contain upper latin letters with optional index
            return False
        if len(atomic) > 1:  # If variable's name contains index
            if not (atomic[1:].isdigit() and not atomic[1] == '0'):  # Index can only be natural number
                return False
        return True

    @classmethod
    def __check_formula_syntax(cls, formula: str):
        if formula == '#':
            return True
        deepest_operation_index = cls.__find_index_of_deepest_operation(formula)
        close_parenthesis_index = formula[deepest_operation_index:].find(')') + deepest_operation_index
        if close_parenthesis_index == -1:
            raise IncorrectFormula('No close parenthesis')
        open_parenthesis_index = formula[:deepest_operation_index].rfind('(')
        if formula[deepest_operation_index] == cls.MACHINERY_SYMBOLS['negation']:
            negation_argument = formula[deepest_operation_index + 1:close_parenthesis_index]
            if not (deepest_operation_index - open_parenthesis_index == 1 and (cls.__is_atomic(negation_argument)
                                                                               or negation_argument == '#')):
                raise IncorrectFormula('Incorrect negation argument')
        else:
            left_argument = formula[open_parenthesis_index + 1:deepest_operation_index]
            right_argument = formula[deepest_operation_index + 1:close_parenthesis_index]
            if not ((cls.__is_atomic(left_argument) or left_argument == '#')
                    and (cls.__is_atomic(right_argument) or right_argument == '#')):
                raise IncorrectFormula('Incorrect binary operation arguments')
        formula = formula[:open_parenthesis_index] + '#' + formula[close_parenthesis_index + 1:]
        cls.__check_formula_syntax(formula)
        return True

    @classmethod
    def __find_index_of_deepest_operation(cls, formula: str):
        deepest_parenthesis_index = formula.rfind('(')
        for i in range(deepest_parenthesis_index, len(formula)):
            if formula[i] in cls.MACHINERY_SYMBOLS.values():
                return i
        raise IncorrectFormula('Incorrect formula')
